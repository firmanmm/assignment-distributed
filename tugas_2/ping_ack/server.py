import server
import datetime

if __name__ == '__main__':
    pyroServer = server.Server("localhost", 7777)
    fileSever = server.FileServer()
    failureDetectorServer = server.FailureDetectorServer(datetime.timedelta(seconds=5))
    pyroServer.Start([fileSever, failureDetectorServer])