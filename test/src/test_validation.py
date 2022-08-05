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
    
    def test_batch_duplicate(self):
        valid_names = [
            "./test/samples/valid/MED_DATA_20220803153932.csv",
            "./test/samples/valid/MED_DATA_20220803153932.csv",
        ]
        invalid_names = [
            "./test/samples/invalid/Bad Data/MED_DATA_20220803160732.csv",
        ]

        for name in invalid_names:
            self.assertFalse(validation.check_batch_id(name))

        for name in valid_names:
            self.assertTrue(validation.check_batch_id(name))