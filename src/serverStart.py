# THIS HAS NO SHUTDOWN COMMAND RIGHT NOW! WILL ADD ONE AS SOON AS I FIGURE OUT HOW TO

# new file to stop relying on filezila

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
import time


def startServer():
    authorizer = DummyAuthorizer()

    authorizer.add_user("user", "password", ".", perm="elradfmwMT")
    # authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "ready!"

    # changed the server around, this now starts a simple ftpserver on 0.0.0.0:12345
    address = ("127.0.0.1", 2121)
    server = servers.FTPServer(address, handler)
    server.serve_forever()


startServer()
time.sleep(5)
# self.close_all()
