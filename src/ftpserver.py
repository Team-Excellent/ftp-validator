from ftplib import FTP
import os

# adds the zip file to the ftpserver
def setup():

    # setup the ftp connection (yeah its in local storage port 21 is blocked on ethernet)
    ftp = FTP()
    # should be runnning through serverStart.py, change those credentials if needed
    ftp.connect(host='127.0.0.1', port=2121)
    ftp.login(user='user', passwd='password')
    # creates the folder to store the samples
    try:
        ftp.cwd('/samples')
    except:
        ftp.mkd('/samples')
        ftp.cwd('/samples')

    os.chdir('test/samples')
    # gets every file in the sample folder
    lst = os.walk(os.getcwd())
    for file in lst:
        print(file[0])
        path = file[0]
        try:
            for csv in file[2]:
                f = open(f'{path}\\{csv}', 'rb')
                ftp.storbinary(f'STOR {csv}', f)
                f.close()
        except:
            continue
        ftp.cwd('\\samples\\')
    os.chdir('..')
# adds the zip file to the ftpserver
def pullSamples(date):
    # another connection! [because when this is run the initial one may have timed out, same stuff though]
    ftp = FTP()
    # should be runnning through serverStart.py, change those credentials if needed
    ftp.connect(host='127.0.0.1', port=2121)
    ftp.login(user='user', passwd='password')
    # should error handle this but there are no circumstances where this is called pre setup
    ftp.cwd('\\samples')
    os.chdir('..')

    try:
        os.chdir('tmp')
    except:
        os.mkdir('tmp')
        os.chdir('tmp')

    files = ftp.nlst()
    returnLst = []
    for x in files:
        if date in x:
            with open(x, 'wb') as fp:
                ftp.retrbinary(f'RETR {x}', fp.write)
    #ftp.cwd('\\samples')
    #ftp.quit()

# for testing!
#setup()
#pullSamples(20220803)
