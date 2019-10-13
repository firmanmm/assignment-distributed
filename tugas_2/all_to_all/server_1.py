import server
import datetime
import all_to_all.listener as listener

if __name__ == '__main__':
    host = "localhost"
    port = 7777
    pyroServer = server.Server(host, port, identifier="FS1-")
    fileSever = server.FileServer()
    broadcastTargets = [
        "PYRONAME:CL-FailureDetectorServer@%s:%d" % (host, port),
        "PYRONAME:FS2-FailureDetectorServer@%s:%d" % (host, port)
    ]

    failureDetectorServer = server.FailureDetectorServer(datetime.timedelta(seconds=5), broadcastTargets=broadcastTargets, identifier="FS1-FileServer")
    fileClient = listener.Listener("CL-FileClient")
    fileServer2 = listener.Listener("FS2-FileServer")
    failureDetectorServer.AddListener(fileClient.GetIdentifier(), fileClient.OnChange, fileClient.OnRecover)
    failureDetectorServer.AddListener(fileServer2.GetIdentifier(), fileServer2.OnChange, fileServer2.OnRecover)
    pyroServer.Start([fileSever, failureDetectorServer])