import unittest
import arcpy
import os

from . import geojson_helper


class GeojsonHelperTestCase(unittest.TestCase):
    MOCK_POINT_SHP = "MOCK_POINT.shp"
    MOCK_POLY_SHP = "MOCK_POLY.shp"

    def setUp(self):
        # set arcpy workspace to mock data directory
        arcpy.env.workspace = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "mock_data",
            )
        )

    def test_feature_class_to_geojson_point(self):
        geojson = geojson_helper.feature_class_to_geojson(self.MOCK_POINT_SHP)

        self.assertEqual(
            geojson,
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": 0,
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -76.49728323840485,
                                42.440759898132285,
                            ],
                        },
                        "properties": {"FID": 0, "name": "test"},
                    }
                ],
            },
        )

    def test_feature_class_to_geojson_polygon(self):
        poly_geojson = geojson_helper.feature_class_to_geojson(self.MOCK_POLY_SHP)

        self.assertEqual(
            poly_geojson,
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": 0,
                        "geometry": {
                            'coordinates': [
                                [
                                    [4.010871834916598, 6.458471631864148],
                                    [4.008658477684712, 6.444809063435961],
                                    [4.026700693703528, 6.4432095190889385],
                                    [4.027505550960454, 6.45720536055499],
                                    [4.010871834916598, 6.458471631864148]
                                ]
                            ],
                            'type': 'Polygon'
                        },
                        "properties": {
                            'DateTime': None,
                            'DoubleValu': 0,
                            'FID': 0,
                            'IntegerVal': 0,
                            'Name': ' ',
                            'Shape_Area': 3017140.08231,
                            'Shape_Leng': 6994.31215638,
                            'Text': ' '
                        },
                    }
                ],
            },
        )
