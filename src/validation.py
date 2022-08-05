from datetime import datetime


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
        print(date.day)
    except ValueError:
        return False

    # Check extension
    if filename[23:] != ".csv":
        return False

    return True


def validate_not_empty(filename):
    with open(filename, "r") as f:
        return len(f.read()) != 0
