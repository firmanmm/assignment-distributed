import Pyro4
import file_manager
import json
import base64
import consistency
import client

class Server:
    def __init__(self, host, port, identifier="main-"):
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
        daemon.requestLoop()

class FileServer:
    def __init__(self, host, port, identifier="main-", syncServer=[]):
        self.server = Server(host, port, identifier)
        self.fileManager = file_manager.FileManager(identifier)
        self.lockSync = consistency.Sync()
        self.syncServer = list()
        for server in syncServer:
            url = "PYRONAME:%s@%s:%d" % (server, host, port)
            self.syncServer.append(Pyro4.Proxy(url))
        self.Sync()


    def Start(self):
        self.server.Start([self])

    def Store(self, fileName, fileContent, cascade = True):
        try:
            fileContent = base64.b64decode(fileContent["data"])
            self.AcquireGlobalModificationLock(fileName)
            self.fileManager.Store(fileName, fileContent)
            self.ReleaseGlobalModificationLock(fileName)
            if cascade:
                for server in self.syncServer:
                    try:
                        server.Store(fileName, fileContent, False)
                    except:
                        pass
        except Exception as e:
            return self.handleError(e)
    
    def Update(self, fileName, fileContent, cascade = True):
        try:
            fileContent = base64.b64decode(fileContent["data"])
            self.AcquireGlobalModificationLock(fileName)
            self.fileManager.Update(fileName, fileContent)
            self.ReleaseGlobalModificationLock(fileName)
            if cascade:
                for server in self.syncServer:
                    try:
                        server.Update(fileName, fileContent, False)
                    except:
                        pass
        except Exception as e:
            return self.handleError(e)

    def Append(self, fileName, fileContent, cascade = True):
        try:
            fileContent = base64.b64decode(fileContent["data"])
            self.AcquireGlobalModificationLock(fileName)
            self.fileManager.Append(fileName, fileContent)
            self.ReleaseGlobalModificationLock(fileName)
            if cascade:
                for server in self.syncServer:
                    try:
                        server.Append(fileName, fileContent, False)
                    except:
                        pass
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

    def Delete(self, fileName, cascade = True):
        try:
            self.AcquireGlobalModificationLock(fileName)
            self.fileManager.Delete(fileName)
            self.ReleaseGlobalModificationLock(fileName)
            if cascade:
                for server in self.syncServer:
                    try:
                        server.Delete(fileName, False)
                    except:
                        pass
        except Exception as e:
            return self.handleError(e)

    def AcquireLock(self, key):
        self.lockSync.AcquireLock(key)
        return "OK"

    def ReleaseLock(self, key):
        self.lockSync.ReleaseLock(key)
        return "OK"

    def AcquireGlobalModificationLock(self, key):
        for server in self.syncServer:
            try:
                server.AcquireLock(key)
            except:
                pass
    
    def ReleaseGlobalModificationLock(self, key):
        for server in self.syncServer:
            try:
                server.ReleaseLock(key)
            except:
                pass

    def Sync(self):
        localFile = self.List()
        for server in self.syncServer:
            try:
                remoteFileList = server.List()
                for lFile in localFile:
                    if lFile not in remoteFileList:
                        self.Delete(lFile, False)
                localFile = self.List()
                for rFile in remoteFileList:
                    if rFile not in localFile:
                        fileData = server.Get(rFile)
                        self.Store(rFile, fileData, False)
                break
            except:
                pass


    def handleError(self, err):
        return {
            "error": str(err)
        }
