import arcpy

from ..utils import geojson_helper


def aoi_parameter():
    param = arcpy.Parameter(
        displayName="Area Of Interest",
        name="aoi",
        datatype="GPFeatureRecordSetLayer",
        parameterType="Required",
        direction="Input",
    )
    param.filter.list = ["Point", "Polygon"]
    return param


def validate_aoi_parameter(parameter):
    if parameter.value is not None:
        if aoi_has_features(parameter.value) == False:
            parameter.setErrorMessage(
                "AOI must contain features. If the feature layer was newly created and contains a valid geometry, this Geoprocessing Form needs to be refreshed in order to register the new geometry."
            )


def aoi_has_features(aoi_selection):
    result = arcpy.GetCount_management(aoi_selection)
    return int(result.getOutput(0)) > 0


def buffer_parameter():
    param = arcpy.Parameter(
        displayName="Buffer (km)",
        name="buffer",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input",
    )
    param.value = 2.5
    param.filter.type = "Range"
    param.filter.list = [1, 5]
    return param


def build_aoi_from_feature_set(feature_set, buffer_km):
    feature_collection = geojson_helper.esri_json_to_geojson(feature_set.JSON)
    return [
        build_aoi_from_geojson_feature(feature, buffer_km)
        for feature in feature_collection["features"]
    ]


def build_aoi_from_feature_class(feature_class, buffer_km):
    feature_collection = geojson_helper.feature_class_to_geojson(feature_class)
    return [
        build_aoi_from_geojson_feature(feature, buffer_km)
        for feature in feature_collection["features"]
    ]


def build_aoi_from_geojson_feature(geojson_feature, buffer_km):
    """
    This function builds an AOI from either a Point or Polygon geojson feature and returns a dict structure compatible
    with the expected IOS request AOI field.

    :param geojson_feature: Either a point or polygon geojson feature to build the AOI dict from
    :param buffer_km: A buffer in km for point AOIs. The buffer is not used for polygon AOIs
    :return: An IOS compatible AOI dict
    :raise: TypeError - if the geojson_feature is not either a point or polygon feature
    """
    feature_type = geojson_feature["geometry"]["type"].lower()

    if feature_type == 'point':
        return build_aoi_from_geojson_point(geojson_feature, buffer_km)
    elif feature_type == 'polygon':
        return build_aoi_from_geojson_polygon(geojson_feature)
    else:
        raise TypeError(
            "AOI geometry must be type Polygon or Point"
        )


def build_aoi_from_geojson_point(point_feature, buffer_km):
    """
    Creates an IOS compatible AOI from the point feature.
    :param point_feature: The point feature to be converted into an IOS compatible AOI
    :param buffer_km: The buffer zone in km to apply to the AOI
    :return: An IOS compatible AOI dict
    """
    return {
        "type": "point",
        "latitude_deg": round(point_feature["geometry"]["coordinates"][1], 5),
        "longitude_deg": round(point_feature["geometry"]["coordinates"][0], 5),
        "radius_km": buffer_km,
    }


def build_aoi_from_geojson_polygon(polygon_feature):
    """
    Creates an IOS compatible AOI from the polygon feature.
    :param polygon_feature: The polygon feature to be converted into an IOS compatible AOI
    :return: An IOS compatible AOI dict
    """
    return {"type": "polygon", "geojson": polygon_feature["geometry"]}


def build_aois_from_aoi_parameters(aoi_parameter, buffer_parameter):
    aoi_param_describe = arcpy.Describe(aoi_parameter.value)
    if aoi_param_describe.dataType == "FeatureRecordSetLayer":
        return build_aoi_from_feature_set(aoi_parameter.value, buffer_parameter.value)
    elif (
        aoi_param_describe.dataType == "ShapeFile"
        or aoi_param_describe.dataType == "FeatureClass"
    ):
        return build_aoi_from_feature_class(
            aoi_param_describe.catalogPath, buffer_parameter.value
        )
    elif aoi_param_describe.dataType == "FeatureLayer":
        return build_aoi_from_feature_class(
            aoi_param_describe.featureClass.catalogPath, buffer_parameter.value
        )
    else:
        raise TypeError(
            "AOI must be type FeatureRecordSetLayer, ShapeFile, FeatureClass, or FeatureLayer"
        )
