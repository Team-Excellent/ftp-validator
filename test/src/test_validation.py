import unittest
from src import validation


class TestValidationMethods(unittest.TestCase):
    def test_validate_name(self):
        valid_names = [
            "MED_DATA_20210505201229.csv",
            "MED_DATA_20200229201229.csv",
        ]
        invalid_names = [
            "MED_DATA_YYYYMMDDHHMMSS.csv",
            "MED_DATA_20210505201229.csd",
            "_MED_DATA_2021050520122.csv",
            "MED_DATA_20210229201229.csv",
            "MED_DATA_20200229206929.csv",
            "MED_DATA_20200229201269.csv",
            "MED_DATA_20200229251229.csv",
        ]

        for name in invalid_names:
            self.assertFalse(validation.validate_filename(name))

        for name in valid_names:
            self.assertTrue(validation.validate_filename(name))
