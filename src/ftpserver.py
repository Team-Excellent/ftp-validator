from ftplib import FTP
import os
import glob

# adds the zip file to the ftpserver
def setup():

    # setup the ftp connection (yeah its in local storage port 21 is blocked on ethernet)
    ftp = FTP()
    # should be runnning through serverStart.py, change those credentials if needed
    ftp.connect(host="127.0.0.1", port=2121)
    ftp.login(user="user", passwd="password")
    # creates the folder to store the samples
    try:
        ftp.cwd("/samples")
    except:
        ftp.mkd("/samples")
        ftp.cwd("/samples")

    os.chdir(os.path.dirname(__file__) + "/../test/samples")
    # gets every file in the sample folder
    lst = glob.glob("**/*.csv", recursive=True)
    for file in lst:
        print(file)
        try:
            f = open(f"{file}", "rb")
            ftp.storbinary(f"STOR {os.path.basename(file)}", f)
            f.close()
        except Exception as e:
            print(e)
            continue
        ftp.cwd("/samples")
    os.chdir("..")


# adds the zip file to the ftpserver
def pullSamples(usr, pass, ip, pt, date, dir):
    # another connection! [because when this is run the initial one may have timed out, same stuff though]
    ftp = FTP()
    # should be runnning through serverStart.py, change those credentials if needed
    ftp.connect(host=ip, port=pt)
    ftp.login(user=usr, passwd=pass)
    # should error handle this but there are no circumstances where this is called pre setup
    ftp.cwd("/samples")
    os.chdir("..")

    try:
        os.chdir(f"./{dir}")
    except:
        os.mkdir(f"./{dir}")
        os.chdir(f"./{dir}")

    files = ftp.nlst()
    returnLst = []
    for x in files:
        if date in x:
            with open(x, "wb") as fp:
                ftp.retrbinary(f"RETR {x}", fp.write)


# for testing!
# setup()
# pullSamples(20220803)
