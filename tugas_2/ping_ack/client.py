import datetime

import client
import server as detector

if __name__ == '__main__':
    clientHandler = client.Client("localhost", 7777)
    clientHandler.Start(["FileServer"])
    fileManager = client.FileManagerClient(clientHandler, "FileServer")
    interval = datetime.timedelta(seconds=5)
    pingTargets = [
        clientHandler.constructURI("FailureDetectorServer")
    ]
    failureDetector = detector.FailureDetectorServer(interval, pingTargets=pingTargets)
    fileManager.RunCLI()
