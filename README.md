# ftp-validator

ftp-validator: sets up an FTPServer containing a collection of csv files, pulls those files into local storage according to the filters below, validates those files inline with the project brief, then archives the successful files, and logs the unsuccessful files.

## Requirements
In order to install the dependencies use the `requirements.txt` file included

`python3 -m pip install -r requirements.txt`

## Usage
`python3 main.py [optional args]`

```
optional arguments:
  -h, --help   show this help message and exit
  --ip IP      user defined ip address for the FTP server (default: 127.0.0.1)
  --gui        use gui (default)
  --no-gui     no gui
  --port PORT  user defined port for the FTP server (default: 21)
  --user USER  username for the FTP server (default: user)
  --pswd PSWD  password for the FTP server (default: password)
  --date DATE  date to validate the files (default: 20220803)
  --dir DIR    output dir to store the validated files
 ```

## Example FTP server
An example FTP server is also included and can be activated by running the `serverStart.py` script

`python3 serverStart.py`

The example server runs on localhost on port 2121. 
The server will contain files for the date 20220803.

Server Details:
- username: user
- password: password


