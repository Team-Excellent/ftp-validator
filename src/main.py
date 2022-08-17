import os.path
from error_logging import Logger
import validation
import ftpserver
from os import listdir
from os.path import isfile, join
from pathlib import Path
import shutil


def check_all(downloaded_file, logger):
    validators = [
        (validation.validate_filename, "file name in invalid format"),
        (validation.check_batch_id, "file contains duplicate batch ids"),
        (validation.validate_not_empty, "file is empty"),
        (
            validation.validate_invalid_entries,
            "file contains invalid data for a record",
        ),
        (validation.check_batch_header, "file headers are invalid"),
        (validation.check_missing_columns, "file contains missing columns"),
    ]
    for validator in validators:
        if not validator[0](downloaded_file):
            logger.log_item(downloaded_file, validator[1])
            return False
    return True


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
    downloads_dir = Path(os.path.join(os.path.dirname(os.getcwd()), "downloads"))
    downloads_dir.mkdir(parents=True, exist_ok=True)
    log = Logger(downloads_dir.joinpath("log.txt"))

    # Start FTP server and upload samples
    ftpserver.setup()

    file_list = grab_files()
    for file in file_list:
        if check_all(file, log):
            print(f"file {file} valid")
            valid_dir = os.path.join(downloads_dir, "valid")
            archive_file(file, valid_dir)
        else:
            print(f"file {file} invalid")
            invalid_dir = os.path.join(downloads_dir, "invalid")
            archive_file(file, invalid_dir)
    shutil.rmtree("../tmp")
