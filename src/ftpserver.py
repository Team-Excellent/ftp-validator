#filezilla admin pword: bepis3000 , user login = user, password = thisisapassword
from ftplib import FTP

#serverip:
ftp = FTP('127.0.0.1')
ftp.login(user='user', passwd = 'thisisapassword')
ftp.mkd('newDir')
ftp.cwd('newDir')
ftp.retrlines('LIST')
