import arcpy


def additional_notes_parameter():
    param = arcpy.Parameter(
        displayName="Additional Notes",
        name="additional_notes",
        datatype="GPString",
        parameterType="Optional",
        direction="Input")

    return param


def is_note_only_spaces(note: str) -> bool:
    """
    This helper function checks to see if the additional notes parameter is only a series of spaces.
    If only spaces are found the helper returns true, if characters other than spaces are found then it
    returns false.
    :param note: A string to check for all spaces
    :return: True if the string only contains spaces or if the str is None, False if it contains other characters
    """
    if note is None:
        return True
    elif all(char == ' ' for char in note):
        return True
    else:
        return False
