import arcpy

def customer_notes_parameter():
    param = arcpy.Parameter(
        displayName="Customer Notes",
        name="customer_notes",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

    return param
