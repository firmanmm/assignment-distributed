import datetime

import client

if __name__ == '__main__':
    clientHandler = client.Client("localhost", 7777)
    clientHandler.Start(["FS1-FileServer"])
    fileManager = client.FileManagerClient(clientHandler, "FS1-FileServer")
    fileManager.RunCLI()
