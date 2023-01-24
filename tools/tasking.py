import datetime
from typing import List

import arcpy

from platform_api import auth_token, ios
from utils import jwt_helper


class Tasking(object):

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tasking"
        self.description = "New Image Tasking"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            self.aoi_parameter(),
            self.buffer_parameter(),
            self.start_date_parameter(),
            self.end_date_parameter(),
            self.imaging_mode_parameter(),
            self.preferred_vendors_parameter()
        ]

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        self.validate_aoi_parameter(parameters[0])
        self.validate_start_date_parameter(parameters[2])
        self.validate_end_date_parameter(parameters[2], parameters[3])

    def execute(self, parameters, messages):
        """The source code of the tool."""
        if jwt_helper.has_role(auth_token.token, 'IOS.Order.Create'):
            messages.addMessage('Building Order...')
            email = jwt_helper.email_from_jwt(auth_token.token)
            order = self.tasking_order_from_parameters(email, parameters)

            messages.addMessage('Submitting Order...')
            resp = ios.post_order(order)

            if resp.status_code == 201:
                self.handle_order_success(resp, messages)
            else:
                self.handle_order_failure(resp, messages)
        else:
            self.handle_l1_user(messages)

    def handle_order_success(self, resp, messages):
        resp_json = resp.json()
        if resp_json['statusHistory'][-1]['state'] == 'in-progress':
            self.handle_invoice_customer(resp_json['id'], messages)
        else:
            self.handle_stripe_customer(resp_json['id'], messages)

    def handle_order_failure(self, resp, messages):
        messages.addErrorMessage({
            'status_code': resp.status_code,
            'reason': resp.reason
        })

    def handle_invoice_customer(self, order_id, messages):
        messages.addMessage('Order Submitted!')
        messages.addMessage('Order Number: {}'.format(order_id))
        messages.addMessage(
            'You will receive an email confirmation with full order details shortly.'
        )

    def handle_stripe_customer(self, order_id, messages):
        ios.cancel_order(order_id)
        messages.addErrorMessage(
            'Must be an invoice customer to submit orders. Please contact support@ursaspace.com.'
        )

    def handle_l1_user(self, messages):
        messages.addErrorMessage(
            'Must be an L2 User to submit orders. Please contact support@ursaspace.com.'
        )

    def aoi_parameter(self):
        param = arcpy.Parameter(
            displayName="Area Of Interest",
            name="aoi",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input",
        )
        param.filter.list = ["Point"]
        return param

    def validate_aoi_parameter(self, parameter):
        if parameter.value is not None:
            if self.aoi_has_features(parameter.value) == False:
                parameter.setErrorMessage(
                    'AOI must contain features. After adding features, clear AOI parameter and re-select layer.'
                )

    def aoi_has_features(self, aoi_selection):
        result = arcpy.GetCount_management(aoi_selection)
        return int(result.getOutput(0)) > 0

    def buffer_parameter(self):
        param = arcpy.Parameter(
            displayName="Buffer (km)",
            name="buffer",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        param.value = 2.5
        param.filter.type = "Range"
        param.filter.list = [1, 5]
        return param

    def start_date_parameter(self):
        param = arcpy.Parameter(
            displayName="Start Date",
            name="startDate",
            datatype="GPDate",
            parameterType="Required",
            direction="Input"
        )
        # give user 1 hour buffer by default to complete order within required 48hr window
        param.value = self.get_minimum_start_date() + datetime.timedelta(hours=1)
        return param

    def validate_start_date_parameter(self, parameter):
        min_date = self.get_minimum_start_date()
        if parameter.value < min_date:
            parameter.setErrorMessage(
                "Minimum Start Date must be {}".format(min_date)
            )

    def end_date_parameter(self):
        param = arcpy.Parameter(
            displayName="End Date",
            name="endDate",
            datatype="GPDate",
            parameterType="Required",
            direction="Input"
        )
        param.value = (self.get_minimum_start_date() +
                       datetime.timedelta(hours=24)).replace(hour=23, minute=59)
        return param

    def validate_end_date_parameter(self, start_parameter, end_parameter):
        if start_parameter.value == end_parameter.value:
            end_parameter.setWarningMessage(
                "Increase range to improve probability of successful order."
            )
        if start_parameter.value > end_parameter.value:
            end_parameter.setErrorMessage(
                "End Date cannot precede Start Date."
            )

    def imaging_mode_parameter(self):
        param = arcpy.Parameter(
            displayName="Imaging Mode",
            name="imagingMode",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param.value = "SPOTLIGHT"
        param.filter.type = 'ValueList'
        param.filter.list = ["SPOTLIGHT", "STRIPMAP"]
        return param

    def preferred_vendors_parameter(self):
        param = arcpy.Parameter(
            displayName="Preferred Vendors",
            name="preferredVendors",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True
        )
        param.filter.type = "ValueList"
        param.filter.list = ["CAPELLA", "ICEYE"]
        return param

    def build_aois_from_aoi_parameters(self, aoi_parameter, buffer_parameter):
        aoi_param_describe = arcpy.Describe(aoi_parameter.value)
        if aoi_param_describe.dataType == "FeatureRecordSetLayer":
            return ios.build_aoi_from_feature_set(
                aoi_parameter.value,
                buffer_parameter.value
            )
        elif aoi_param_describe.dataType == 'ShapeFile' or aoi_param_describe.dataType == 'FeatureClass':
            return ios.build_aoi_from_feature_class(
                aoi_param_describe.catalogPath,
                buffer_parameter.value
            )
        elif aoi_param_describe.dataType == 'FeatureLayer':
            return ios.build_aoi_from_feature_class(
                aoi_param_describe.featureClass.catalogPath,
                buffer_parameter.value
            )
        else:
            raise TypeError(
                'AOI must be type FeatureRecordSetLayer, ShapeFile, FeatureClass, or FeatureLayer'
            )

    def tasking_order_from_parameters(self, email: str, parameters: List[arcpy.Parameter]):
        aoi = self.build_aois_from_aoi_parameters(
            aoi_parameter=parameters[0],
            buffer_parameter=parameters[1]
        )

        schedule = ios.build_schedule(
            start_date=parameters[2].value,
            end_date=parameters[3].value
        )

        mode = ios.build_imaging_mode(
            mode=parameters[4].value
        )

        resolution = ios.build_resolution_meters(
            mode=parameters[4].value
        )

        vendors = ios.build_vendor_preferences(
            vendors=parameters[5].values
        )

        collection_parameters = ios.build_collection_parameters(
            imaging_mode=mode,
            resolution_meters=resolution,
            vendor_preferences=vendors
        )

        ios_order = ios.build_tasking_order(
            email=email,
            aois=aoi,
            schedule=schedule,
            params=collection_parameters
        )

        return ios_order

    def get_minimum_start_date(self):
        return datetime.datetime.now() + datetime.timedelta(hours=48)
