import os.path

import validation
import ftpserver
from os import listdir
from os.path import isfile, join
from pathlib import Path
import shutil


def check_all(downloaded_file):
    passed = validation.validate_filename(downloaded_file)
    passed = validation.check_batch_id(downloaded_file) and passed
    passed = validation.validate_not_empty(downloaded_file) and passed
    passed = validation.validate_invalid_entries(downloaded_file) and passed
    passed = validation.check_batch_header(downloaded_file) and passed
    passed = validation.check_missing_columns(downloaded_file) and passed
    return passed


# grab files from tmp
def grab_files():
    ftpserver.pullSamples("20220803")
    file_list = [f for f in listdir(os.getcwd())]
    return file_list


def archive_file(file, out_dir):
    filename = os.path.basename(file)
    year = filename[9:13]
    month = filename[13:15]
    day = filename[15:17]
    directory = Path(out_dir, year, month, day)
    directory.mkdir(parents=True, exist_ok=True)

    shutil.copy(file, directory.joinpath(file))

    print(filename)


# main function
if __name__ == "__main__":
    # Start FTP server and upload samples
    ftpserver.setup()

    file_list = grab_files()
    for file in file_list:
        if check_all(file):
            print(f"file {file} valid")
            valid_dir = os.path.join(os.path.dirname(os.getcwd()), "downloads", "valid")
            archive_file(file, valid_dir)
        else:
            print(f"file {file} invalid")
            invalid_dir = os.path.join(
                os.path.dirname(os.getcwd()), "downloads", "invalid"
            )
            archive_file(file, invalid_dir)
