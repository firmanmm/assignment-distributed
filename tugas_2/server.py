import Pyro4
import file_manager
import json
import base64

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
    def __init__(self, host, port, identifier="main-"):
        self.server = Server(host, port, identifier)
        self.fileManager = file_manager.FileManager()

    def Start(self):
        self.server.Start([self])

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

if __name__ == '__main__':
    server = FileServer("localhost", 7777)
    server.Start()
