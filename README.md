# ftp-validator

ftp-validator: sets up an FTPServer containing a collection of csv files, pulls those files into local storage according to the filters below, validates those files inline with the project brief, then archives the successful files, and logs the unsuccessful files.


## usage
main.py [-h] [--ip IP] [--port PORT] [--user USER] [--pswd PSWD] [--date DATE] [--dir DIR]

options:
  -h, --help   show this help message and exit
  --ip IP      user defined ip address for the FTP server (default: 127.0.0.1)
  --port PORT  user defined port for the FTP server (default: 21)
  --user USER  username for the FTP server (default: user)
  --pswd PSWD  password for the FTP server (default: password)
  --date DATE  date to validate the files (default: 20220803)
  --dir DIR    output dir to store the validated files (default: tmp)
