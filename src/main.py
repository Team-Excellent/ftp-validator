from datetime import datetime
from datetime import timedelta
import os.path
from error_logging import Logger
import validation
import ftpserver
from os import listdir
from os.path import isfile, join
from pathlib import Path
import shutil
import argparse
import ftplib
import socket
import gui


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
def grab_files(date, usr, pswd, ip, pt):

    ftpserver.pullSamples(usr, pswd, ip, pt, date.strftime("%Y%m%d"), "tmp")
    file_list = [f for f in listdir(os.getcwd()) if date.strftime("%Y%m%d") in f]
    return file_list


def archive_file(file, out_dir):
    filename = os.path.basename(file)
    year = filename[9:13]
    month = filename[13:15]
    day = filename[15:17]
    directory = Path(out_dir, year, month, day)
    directory.mkdir(parents=True, exist_ok=True)

    shutil.copy(file, directory.joinpath(file))


# main function
def download_files(output_dir, start_date, end_date, usr, pswd, ip, pt):
    if output_dir == "":
        raise FileNotFoundError
    downloads_dir = Path(os.path.join(output_dir, "downloads"))
    if (len(output_dir) == 1 and output_dir != "/") or (
        output_dir[0] != "/" and output_dir[1] != ":"
    ):
        downloads_dir = Path(os.getcwd()).joinpath(downloads_dir)

    downloads_dir.mkdir(parents=True, exist_ok=True)
    log = Logger(downloads_dir.joinpath("log.txt"))

    invalid_files = False

    # Start FTP server and upload samples
    ftpserver.setup()
    file_list = []
    diff = end_date - start_date

    for i in range(diff.days + 1):
        day = start_date + timedelta(days=i)
        file_list += grab_files(day, usr, pswd, ip, pt)

    for file in file_list:
        if check_all(file, log):
            valid_dir = os.path.join(downloads_dir, "valid")
            archive_file(file, valid_dir)
        else:
            invalid_files = True
            invalid_dir = os.path.join(downloads_dir, "invalid")
            archive_file(file, invalid_dir)
    shutil.rmtree("../tmp")

    return invalid_files


if __name__ == "__main__":
    # cli stuff happy for this to be moved around if needed
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        help="user defined ip address for the FTP server (default: 127.0.0.1)",
        default="127.0.0.1",
    )
    parser.add_argument(
        "--gui", dest="gui", action="store_true", help="use gui (default)"
    )
    parser.add_argument("--no-gui", dest="gui", action="store_false", help="no gui")
    parser.set_defaults(gui=True)
    parser.add_argument(
        "--port",
        help="user defined port for the FTP server (default: 21)",
        default="21",
    )
    parser.add_argument(
        "--user", help="username for the FTP server (default: user)", default="user"
    )
    parser.add_argument(
        "--pswd",
        help="password for the FTP server (default: password)",
        default="password",
    )
    parser.add_argument(
        "--date",
        help="date to validate the files (default: 20220803)",
        default="20220803",
    )
    parser.add_argument(
        "--dir",
        help="output dir to store the validated files",
        default=".",
    )
    args = parser.parse_args()
    if args.gui:
        gui.main()
        exit(0)
    start_date = datetime.strptime(args.date, "%Y%m%d")
    try:
        download_files(
            start_date=start_date,
            end_date=start_date,
            usr=args.user,
            pswd=args.pswd,
            ip=args.ip,
            pt=int(args.port),
            output_dir=args.dir,
        )
        saved_dir = args.dir
        if not os.path.isabs(args.dir):
            saved_dir = Path(__file__).parent.joinpath(saved_dir).joinpath("downloads")
        print(f"Downloaded succeeded, files saved to {saved_dir}")
    except ConnectionRefusedError:
        print("Connection refused, is the ip/port correct?")
    except FileNotFoundError:
        print("Invalid output directory")
    except ftplib.error_perm:
        print("Incorrect credentials")
    except socket.timeout:
        print("Connection timed out (are details correct?)")
    except Exception as e:
        print("Error Occurred")
        print(e)
