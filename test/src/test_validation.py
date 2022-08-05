import unittest
from src import validation
import os
import glob


class TestValidationMethods(unittest.TestCase):
    @staticmethod
    def remove_files(files):
        for file in files:
            os.remove(file)

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

    def test_validate_not_empty(self):
        # Invalid file
        self.addCleanup(self.remove_files, ["temp.txt"])
        with open("temp.txt", "w") as f:
            self.assertFalse(validation.validate_not_empty("temp.txt"))

        # Valid file
        with open("temp.txt", "w") as f:
            f.write("Here is some text")

        self.assertTrue(validation.validate_not_empty("temp.txt"))

    def test_batch_header(self):
        valid_names = [
            "./test/samples/valid/MED_DATA_20220803153932.csv",
            "./test/samples/valid/MED_DATA_20220803153932.csv",
        ]
        invalid_names = [
            "./test/samples/invalid/Bad Header/MED_DATA_20220803155853.csv",
        ]

        for name in invalid_names:
            self.assertFalse(validation.check_batch_header(name))

        for name in valid_names:
            self.assertTrue(validation.check_batch_header(name))

    def test_missing_columns(self):
        valid_names = [
            "./test/samples/valid/MED_DATA_20220803153932.csv",
            "./test/samples/valid/MED_DATA_20220803153932.csv",
        ]
        invalid_names = [
            "./test/samples/invalid/Bad Data/MED_DATA_20220803160730.csv",
        ]

        for name in invalid_names:
            self.assertFalse(validation.check_missing_columns(name))

        for name in valid_names:
            self.assertTrue(validation.check_missing_columns(name))

    def test_validate_invalid_entries(self):
        invalid_files = glob.glob("./test/samples/invalid/Bad Data/*.csv")
        valid_files = glob.glob("./test/samples/valid/*.csv")

        for file in invalid_files:
            print(file)
            self.assertFalse(validation.validate_invalid_entries(file))

        for file in valid_files:
            self.assertTrue(validation.validate_invalid_entries(file))
