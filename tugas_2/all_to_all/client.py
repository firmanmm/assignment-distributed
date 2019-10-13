import datetime
import all_to_all.listener as listener
import threading

import client
import server

if __name__ == '__main__':
    host = "localhost"
    port = 7777
    pyroServer = server.Server(host, port, identifier="CL-")
    clientHandler = client.Client(host, port)
    clientHandler.Start(["FS1-FileServer"])
    broadcastTargets = [
        "PYRONAME:FS1-FailureDetectorServer@%s:%d" % (host, port),
        "PYRONAME:FS2-FailureDetectorServer@%s:%d" % (host, port)
    ]
    failureDetectorServer = server.FailureDetectorServer(datetime.timedelta(seconds=5), identifier="CL-FileClient", broadcastTargets=broadcastTargets)
    fileServer1 = listener.Listener("FS1-FileServer")
    fileServer2 = listener.Listener("FS2-FileServer")
    failureDetectorServer.AddListener(fileServer1.GetIdentifier(), fileServer1.OnChange, fileServer1.OnRecover)
    failureDetectorServer.AddListener(fileServer2.GetIdentifier(), fileServer2.OnChange, fileServer2.OnRecover)
    fileManager = client.FileManagerClient(clientHandler, "FS1-FileServer")
    thread = threading.Thread(target=pyroServer.Start, args=([failureDetectorServer],))
    thread.daemon = True
    thread.start()
    fileManager.RunCLI()
