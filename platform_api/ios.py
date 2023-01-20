import datetime
from typing import List

import requests

import config
from utils import geojson_helper

from . import auth_token


def post_order(order_object):
    headers = {
        "Authorization": "Bearer {}".format(auth_token.token),
        "Content-Type": "application/json",
    }

    order_url = "{}/api/ios/order".format(config.baseUrl)

    return requests.post(
        url=order_url,
        headers=headers,
        json=order_object,
    )


def build_aoi_from_feature_set(feature_set, buffer_km):
    feature_collection = geojson_helper.esri_json_to_geojson(feature_set.JSON)
    return [
        build_aoi_from_geojson_feature(
            feature,
            buffer_km
        ) for feature in feature_collection['features']
    ]


def build_aoi_from_feature_class(feature_class, buffer_km):
    feature_collection = geojson_helper.feature_class_to_geojson(feature_class)
    return [
        build_aoi_from_geojson_feature(
            feature,
            buffer_km
        ) for feature in feature_collection['features']
    ]


def build_aoi_from_geojson_feature(point_feature, buffer_km):
    return {
        "type": "point",
        "latitude_deg": round(point_feature['geometry']['coordinates'][1], 5),
        "longitude_deg": round(point_feature['geometry']['coordinates'][0], 5),
        "radius_km": buffer_km
    }


def build_schedule(start_date: datetime.date, end_date: datetime.date):
    return [{
        "type": "range",
        "range": {
            "min": start_date.isoformat(),
            "max": end_date.isoformat()
        }
    }]


def build_imaging_mode(mode: str):
    return {
        "constraint": mode,
        "level": "required"
    }


def resolution_from_mode(mode: str):
    if mode == 'SPOTLIGHT':
        return {
            "min": 0.5,
            "max": 1.5
        }
    elif mode == 'STRIPMAP':
        return {
            "min": 0.5,
            "max": 3.5
        }
    else:
        return None


def build_resolution_meters(mode: str):
    resolution_obj = resolution_from_mode(mode)
    if resolution_obj != None:
        return {
            "constraint": resolution_obj,
            "level": "required"
        }
    else:
        return None


def build_vendor_preferences(vendors: List[str]):
    obj = {}

    if vendors is not None:
        for vendor in vendors:
            obj[vendor] = "preferred"

    return obj


def build_collection_parameters(
    imaging_mode,
    resolution_meters,
    vendor_preferences
):
    return [{
        "type": "sar",
        "imagingMode": imaging_mode,
        "resolutionMeters": resolution_meters,
        "vendorPreferences": vendor_preferences
    }]


def build_tasking_order(email, aois, schedule, params):
    return {
        "customerNotes": "#ESRI-TOOLBOX",
        "request": {
            "contactEmail": email,
            "requireApproval": True,
            "type": "tasking-parameters",
            "aois": aois,
            "schedule": schedule,
            "collectionParameters": params
        }
    }
