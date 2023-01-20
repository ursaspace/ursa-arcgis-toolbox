import datetime
import os
import unittest

import arcpy

from . import ios


class IosTestCase(unittest.TestCase):

    MOCK_FEATURE_CLASS = 'MOCK_POINT.shp'
    MOCK_BUFFER = 2

    def setUp(self):
        # set arcpy workspace to mock data directory
        arcpy.env.workspace = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "mock_data",
            )
        )

    def test_build_aoi_from_feature_set(self):
        # create feature set from mock feature class
        MOCK_FEATURE_SET = arcpy.FeatureSet(
            self.MOCK_FEATURE_CLASS
        )

        aoi = ios.build_aoi_from_feature_set(
            MOCK_FEATURE_SET,
            self.MOCK_BUFFER
        )

        self.assertEqual(
            aoi,
            [{
                "type": "point",
                "latitude_deg": 42.44076,
                "longitude_deg": -76.49728,
                "radius_km": self.MOCK_BUFFER
            }]
        )

    def test_build_aoi_from_feature_class(self):
        aoi = ios.build_aoi_from_feature_class(
            self.MOCK_FEATURE_CLASS,
            self.MOCK_BUFFER
        )

        self.assertEqual(
            aoi,
            [{
                "type": "point",
                "latitude_deg": 42.44076,
                "longitude_deg": -76.49728,
                "radius_km": self.MOCK_BUFFER
            }]
        )

    def test_build_aoi_from_geojson_feature(self):
        MOCK_GEOJSON_FEATURE = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [0, 1]
            },
            "properties": {}
        }

        aoi = ios.build_aoi_from_geojson_feature(
            MOCK_GEOJSON_FEATURE,
            self.MOCK_BUFFER
        )

        self.assertEqual(
            aoi,
            {
                "type": "point",
                "latitude_deg": 1,
                "longitude_deg": 0,
                "radius_km": self.MOCK_BUFFER
            }
        )

    def test_build_schedule(self):
        MOCK_START = datetime.datetime(1, 1, 1)
        MOCK_END = datetime.datetime(1, 1, 2)
        self.assertEqual(
            ios.build_schedule(MOCK_START, MOCK_END),
            [{
                "type": "range",
                "range": {
                    "min": MOCK_START.isoformat(),
                    "max": MOCK_END.isoformat()
                }
            }]
        )

    def test_build_imaging_mode(self):
        MOCK_MODE = "SPOTLIGHT"
        self.assertEqual(
            ios.build_imaging_mode(MOCK_MODE),
            {
                "constraint": MOCK_MODE,
                "level": "required"
            }
        )

    def test_build_resolution_meters(self):
        # if mode is SPOTLIGHT
        self.assertEqual(
            ios.build_resolution_meters('SPOTLIGHT'),
            {
                "constraint": {
                    "min": 0.5,
                    "max": 1.5
                },
                "level": "required"
            })

        # if mode is STRIPMAP
        self.assertEqual(
            ios.build_resolution_meters('STRIPMAP'),
            {
                "constraint": {
                    "min": 0.5,
                    "max": 3.5
                },
                "level": "required"
            })

    def test_build_vendor_preferences(self):
        MOCK_VENDOR_1 = 'VENDOR_1'
        MOCK_VENDOR_2 = 'VENDOR_2'
        MOCK_VENDOR_3 = 'VENDOR_3'

        self.assertEqual(
            ios.build_vendor_preferences([
                MOCK_VENDOR_1,
                MOCK_VENDOR_2,
                MOCK_VENDOR_3
            ]),
            {
                MOCK_VENDOR_1: "preferred",
                MOCK_VENDOR_2: "preferred",
                MOCK_VENDOR_3: "preferred"
            }
        )
