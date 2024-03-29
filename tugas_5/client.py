import Pyro4
import os
import json
import base64

class Client:
    def __init__(self, host, port, identifier = "main-"):
        self.host = host
        self.port = port
        self.identifier = identifier
        self.objects = dict()

    def Start(self, remoteObject):
        for obj in remoteObject:
            url = "PYRONAME:%s%s@%s:%d" % (self.identifier, obj, self.host, self.port)
            self.objects[obj] = Pyro4.Proxy(url)

    def GetObject(self, name):
        return self.objects[name]

class FileManagerClient:

    def __init__(self, host, port, identifier="main-"):
        workDir = os.getcwd()
        self.client = Client(host, port, identifier)
        self.client.Start(["FileServer"])
        self.fileManager = self.client.GetObject("FileServer")
        self.workDir = "%s/%sclient" % (workDir, identifier)
        os.makedirs(self.workDir, exist_ok=True)

    def RunCLI(self):
        while True:
            inData = input("[STORE, UPDATE, APPEND, GET, LIST, DELETE] : ")
            try:
                if inData == "STORE":
                    fileName = input("File Name : ")
                    self.Store(fileName)
                elif inData == "UPDATE":
                    fileName = input("File Name : ")
                    self.Update(fileName)
                elif inData == "APPEND":
                    fileName = input("File Name : ")
                    self.Append(fileName)
                elif inData == "GET":
                    fileName = input("File Name : ")
                    self.Get(fileName)
                elif inData == "LIST":
                    self.List()
                elif inData == "DELETE":
                    fileName = input("File Name : ")
                    self.Delete(fileName)
                else:
                    raise Exception("Command not found!")
            except Exception as e:
                print(str(e))
                    

    def Store(self, fileName):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if not os.path.exists(targetFile):
            raise Exception("File %s couldn't be found" % (fileName))
        fd = open(targetFile, "rb")
        content = fd.read()
        fd.close()
        response = self.fileManager.Store(fileName, content)
        self.handleError(response)

    def Update(self, fileName):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if not os.path.exists(targetFile):
            raise Exception("File %s couldn't be found" % (fileName))
        fd = open(targetFile, "rb")
        content = fd.read()
        fd.close()
        response = self.fileManager.Update(fileName, content)
        self.handleError(response)
        

    def Append(self, fileName):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if not os.path.exists(targetFile):
            raise Exception("File %s couldn't be found" % (fileName))
        fd = open(targetFile, "rb")
        content = fd.read()
        fd.close()
        response = self.fileManager.Append(fileName, content)
        self.handleError(response)
    
    def Get(self, fileName):
        content = self.fileManager.Get(fileName)
        self.handleError(content)
        targetFile = "%s/%s" % (self.workDir, fileName)
        fd = open(targetFile, "wb")
        fd.write(base64.b64decode(content["data"]))
        fd.close()

    def List(self):
        response = self.fileManager.List()
        self.handleError(response)
        for data in response:
            print("Found : %s" % (data))
    
        
    def Delete(self, fileName):
        response = self.fileManager.Delete(fileName)
        self.handleError(response)
    
    def handleError(self, response):
        if type(response) is dict and "error" in response:
            raise Exception(response["error"])