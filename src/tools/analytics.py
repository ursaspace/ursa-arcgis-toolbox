import importlib
from typing import List

import arcpy

from ..utils import jwt_helper
from ..platform_api import auth_token, ios
from ..parameters import aoi, analytic_options, schedule, additional_notes


class Analytics(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Analytics"
        self.description = "Analytics Ordering"
        self.canRunInBackground = False

        # trigger reload for hmr development
        importlib.reload(jwt_helper)
        importlib.reload(ios)
        importlib.reload(aoi)
        importlib.reload(analytic_options)
        importlib.reload(schedule)
        importlib.reload(additional_notes)

    def getParameterInfo(self):
        """Define parameter definitions"""
        return [
            aoi.aoi_parameter(),
            aoi.buffer_parameter(),
            schedule.start_date_parameter(),
            schedule.end_date_parameter(),
            additional_notes.additional_notes_parameter(),
            analytic_options.analytics_parameter(),
            analytic_options.change_detection_parameter(),
        ]

    def updateParameters(self, parameters):
        """Modify the values/properties of parameters before internal
        validation is performed. This method is called whenever a
        parameter has been changed."""
        analytic_options.check_to_enable_cd_param(parameters[5], parameters[6])

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        aoi.validate_aoi_parameter(parameters[0])
        schedule.validate_end_date_parameter(parameters[2], parameters[3])

    def execute(self, parameters, messages):
        """The source code of the tool."""
        if jwt_helper.has_role(auth_token.token, "IOS.Order.Create"):
            messages.addMessage("Building Order...")
            email = jwt_helper.email_from_jwt(auth_token.token)
            order = self.analytics_order_from_parameters(email, parameters)

            messages.addMessage("Submitting Order...")
            resp = ios.post_order(order)

            if resp.status_code == 201:
                ios.handle_order_success(resp, messages)
            else:
                ios.handle_order_failure(resp, messages)
        else:
            ios.handle_l1_user(messages)

    def analytics_order_from_parameters(
        self, email: str, parameters: List[arcpy.Parameter]
    ):
        aoi_obj = aoi.build_aois_from_aoi_parameters(
            aoi_parameter=parameters[0], buffer_parameter=parameters[1]
        )

        schedule_obj = schedule.build_schedule(
            start_date=parameters[2].value, end_date=parameters[3].value
        )

        additional_notes_obj = parameters[4].value
        if additional_notes.is_note_only_spaces(additional_notes_obj):
            additional_notes_obj = None

        workflow_request_obj = analytic_options.build_workflow_request(
            parameters[5].values
        )

        cd_params_obj = (
            analytic_options.build_cd_analytic_params(parameters[6].values)
            if "ChangeDetection" in workflow_request_obj["analytics"]
            else None
        )

        ios_order = ios.build_analytics_order(
            email=email,
            aois=aoi_obj,
            schedule=schedule_obj,
            workflow_request=workflow_request_obj,
            cd_params=cd_params_obj,
            additional_notes=additional_notes_obj,
        )

        return ios_order
