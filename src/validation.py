from datetime import datetime
import csv


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


def check_batch_id(filename):
    """returns whether a given file has duplicate batch ids"""

    #open file and put data in list
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    #for every batch id, check no common batch id's exist
    for i in range (0, len(data)):
        current = data[i][0]
        for j in range (0, len(data)):
            if current == data[j][0] and j != i:
                return False
    
    return True

def validate_not_empty(filename):
    with open(filename, "r") as f:
        return len(f.read()) != 0

def check_batch_header(filename):
    """checks wether a given file has the correct CSV headers"""

    #open file and put data in list
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    #check first list which contains headers with ideal header list
    ideal_headers = ["batch_id", "timestamp", "reading1","reading2","reading3","reading4","reading5","reading6","reading7","reading8","reading9","reading10"]
    if data[0] != ideal_headers:
        return False
    
    return True

def check_missing_columns(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    """Check if all lists in dataset contain the same number of items"""
    for i in data:
        if len(i) != 12:
            return False

    return True