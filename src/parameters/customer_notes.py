import arcpy

def customer_notes_parameter():
    param = arcpy.Parameter(
        displayName="Customer Notes",
        name="customer_notes",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

    return param

def validate_customer_notes_parameter():
    pass

def build_customer_notes():
    pass