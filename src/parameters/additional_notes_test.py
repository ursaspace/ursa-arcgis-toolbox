import unittest
import arcpy
from . import additional_notes


class AdditionalNotesTestCase(unittest.TestCase):

    def test_space_check(self):
        # Validate that a note with characters and a space does not trigger the spaces check
        note_str = "Test Notes"
        self.assertFalse(additional_notes.is_note_only_spaces(note_str))

        # Validate that a note with a single space triggers the space check
        note_str = " "
        self.assertTrue(additional_notes.is_note_only_spaces(note_str))

        # Validate that a note with multiple space triggers the space check
        note_str = "   "
        self.assertTrue(additional_notes.is_note_only_spaces(note_str))

        # Validate that a note that is None returns true
        note_str = None
        self.assertTrue(additional_notes.is_note_only_spaces(note_str))
