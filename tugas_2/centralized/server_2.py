import server
import datetime

if __name__ == '__main__':
    host = "localhost"
    port = 7777
    pyroServer = server.Server(host, port, identifier="FS2-")
    fileSever = server.FileServer()
    broadcastTargets = [
        "PYRONAME:FailureDetectorServer@%s:%d" % (host, port)
    ]
    failureDetectorServer = server.FailureDetectorServer(datetime.timedelta(seconds=5), broadcastTargets=broadcastTargets, identifier="FS2-FileServer")
    pyroServer.Start([fileSever])