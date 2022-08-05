from datetime import datetime
import csv
import re


def validate_filename(filename):
    """Returns whether a given filename is in a valid format"""

    # Check length
    if len(filename) != 27:
        return False

    # Check prefix
    if filename[:9] != "MED_DATA_":
        return False

    # Check date
    try:
        date_format = "%Y%m%d%H%M%S"
        date = datetime.strptime(filename[9:23], date_format)
    except ValueError:
        return False

    # Check extension
    if filename[23:] != ".csv":
        return False

    return True


def check_batch_id(filename):
    """returns whether a given file has duplicate batch ids"""

    # open file and put data in list
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    # for every batch id, check no common batch id's exist
    for i in range(0, len(data)):
        current = data[i][0]
        for j in range(0, len(data)):
            if current == data[j][0] and j != i:
                return False

    return True


def validate_not_empty(filename):
    with open(filename, "r") as f:
        return len(f.read()) != 0


def validate_invalid_entries(filename):
    time_format = "%H:%M:%S"
    value_re = re.compile(r"^[0-9]{1}\.[0-9]{1,3}$")
    with open(filename, "r") as f:
        file_reader = csv.reader(f)
        row_num = 0
        # Check all entries on every row except first
        for idx, row in enumerate(file_reader):
            if idx == 0:
                continue
            # Check batch id
            if not row[0].isnumeric():
                return False

            # Check timestamp
            try:
                datetime.strptime(row[1], time_format)
            except (ValueError, IndexError):
                return False

            # Check readings
            try:
                for reading in row[2:]:
                    if value_re.fullmatch(reading) is None:
                        return False
            except IndexError:
                return False

            return True
