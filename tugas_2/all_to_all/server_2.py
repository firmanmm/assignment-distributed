import server
import datetime
import all_to_all.listener as listener

if __name__ == '__main__':
    host = "localhost"
    port = 7777
    pyroServer = server.Server(host, port, identifier="FS2-")
    fileSever = server.FileServer()
    broadcastTargets = [
        "PYRONAME:CL-FailureDetectorServer@%s:%d" % (host, port),
        "PYRONAME:FS1-FailureDetectorServer@%s:%d" % (host, port)
    ]

    failureDetectorServer = server.FailureDetectorServer(datetime.timedelta(seconds=5), broadcastTargets=broadcastTargets, identifier="FS2-FileServer")
    fileClient = listener.Listener("CL-FileClient")
    fileServer1 = listener.Listener("FS1-FileServer")
    failureDetectorServer.AddListener(fileClient.GetIdentifier(), fileClient.OnChange)
    failureDetectorServer.AddListener(fileServer1.GetIdentifier(), fileServer1.OnChange)
    pyroServer.Start([fileSever, failureDetectorServer])