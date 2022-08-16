import os.path

import validation
import ftpserver
from os import listdir
from os.path import isfile, join


# check file names for easy hits


def check_all(downloaded_file):
    # TODO: Add checks for all validation methods
    return validation.validate_filename(downloaded_file)


# grab files from tmp
def grab_files():
    ftpserver.pullSamples("20220803")
    file_list = [f for f in listdir(os.getcwd())]
    return file_list


# main function
if __name__ == "__main__":
    # Start FTP server and upload samples
    ftpserver.setup()

    file_list = grab_files()
    for i in file_list:
        if check_all(i):
            print(f"file {i} valid")
        else:
            print(f"file {i} invalid")
