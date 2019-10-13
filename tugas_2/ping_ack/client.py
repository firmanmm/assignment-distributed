import base64
import datetime
import json
import os

import Pyro4

import client
import server as detector

if __name__ == '__main__':
    clientHandler = client.Client("localhost", 7777)
    clientHandler.Start(["FileServer"])
    fileManager = client.FileManagerClient(clientHandler)
    interval = datetime.timedelta(seconds=5)
    pingTargets = [
        clientHandler.constructURI("FailureDetectorServer")
    ]
    failureDetector = detector.FailureDetectorServer(interval, pingTargets=pingTargets)
    fileManager.RunCLI()
