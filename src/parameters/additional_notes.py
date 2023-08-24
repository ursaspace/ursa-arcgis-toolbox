import arcpy


def additional_notes_parameter():
    param = arcpy.Parameter(
        displayName="Additional Notes",
        name="additional_notes",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

    return param
