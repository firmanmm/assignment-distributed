import Pyro4
import file_manager
import json
import base64
import pyro_failure_detector as failure_detector
import datetime
import time
import threading

class Server:
    def __init__(self, host, port, identifier=""):
        self.host = host
        self.port = port
        self.identifier = identifier

    def Start(self, objects):
        daemon = Pyro4.Daemon(self.host)
        ns = Pyro4.locateNS(self.host, self.port)
        for obj in objects:
            Pyro4.expose(obj.__class__)
            objAddress = daemon.register(obj)
            ns.register("%s%s" % (self.identifier, type(obj).__name__), objAddress)
        print("Listen and Serve")
        daemon.requestLoop()

class FileServer:
    def __init__(self):
        self.fileManager = file_manager.FileManager()

    def Store(self, fileName, fileContent):
        try:
            fileContent = base64.b64decode(fileContent["data"])
            self.fileManager.Store(fileName, fileContent)
        except Exception as e:
            return self.handleError(e)
    
    def Update(self, fileName, fileContent):
        try:
            fileContent = base64.b64decode(fileContent["data"])
            self.fileManager.Update(fileName, fileContent)
        except Exception as e:
            return self.handleError(e)

    def Append(self, fileName, fileContent):
        try:
            fileContent = base64.b64decode(fileContent["data"])
            self.fileManager.Append(fileName, fileContent)
        except Exception as e:
            return self.handleError(e)

    def Get(self, fileName):
        try:
            content = self.fileManager.Get(fileName)
            return {
                "data": base64.b64encode(content).decode('utf-8')
            }
        except Exception as e:
            return self.handleError(e)

    def List(self):
        try:
            return self.fileManager.List()
        except Exception as e:
            return self.handleError(e)

    def Delete(self, fileName):
        try:
            self.fileManager.Delete(fileName)
        except Exception as e:
            return self.handleError(e)

    def handleError(self, err):
        return {
            "error": str(err)
        }

@Pyro4.expose
class FailureDetectorServer(failure_detector.PyroFailureDetector):
    def __init__(self, deltaTime: datetime.timedelta, identifier = "MAIN-FD", broadcastTargets=[], pingTargets=[]):
        self.broadcastTargets = broadcastTargets
        self.pingTargets = pingTargets
        self.deltaTime = deltaTime
        super().__init__(identifier, deltaTime)
        self.__run__daemon__()
        thread = threading.Thread(target=self.__check__daemon__)
        thread.daemon = True
        thread.start()

    def __check__daemon__(self):
        print("Daemon is running")
        sleepDuration = self.deltaTime.total_seconds()
        while True:
            time.sleep(sleepDuration)
            self.Broadcast(self.broadcastTargets)
            currentTime = datetime.datetime.now()
            for target in self.pingTargets:
                if not self.Ping(target):
                    print("[%s][PING] Service %s is down!" % (currentTime.strftime("%m/%d/%Y, %H:%M:%S"),target))
                
    def Ack(self):
        return super().Ack()
    
    def OnNotify(self, host):
        return super().OnNotify(host)