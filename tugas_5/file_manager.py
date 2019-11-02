import os
import pathlib

class FileException(Exception):
    pass

class FileManager:

    def __init__(self, prefix = ""):
        workDir = os.getcwd()
        self.workDir = "%s/%sserver" % (workDir, prefix)  
        os.makedirs(self.workDir, exist_ok=True)
    
    def Store(self, fileName, fileContent):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if os.path.isfile(targetFile):
            raise FileException("File %s already exist" % (fileName))
        descriptor = open(targetFile, "wb")
        descriptor.write(fileContent)
        descriptor.close()

    def Update(self, fileName, fileContent):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if not os.path.isfile(targetFile):
            raise FileException("File %s not exist" % (fileName))
        descriptor = open(targetFile, "wb")
        descriptor.truncate()
        descriptor.write(fileContent)
        descriptor.close()


    def Append(self, fileName, fileContent):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if not os.path.isfile(targetFile):
            raise FileException("File %s not exist" % (fileName))
        descriptor = open(targetFile, "ab")
        descriptor.write(fileContent)
        descriptor.close()

    def Get(self, fileName):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if not os.path.isfile(targetFile):
            raise FileException("File %s not exist" % (fileName))
        descriptor = open(targetFile, "rb")
        content = descriptor.read()
        descriptor.close()
        return content

    def List(self):
        return os.listdir(self.workDir)

    def Delete(self, fileName):
        targetFile = "%s/%s" % (self.workDir, fileName)
        if not os.path.isfile(targetFile):
            raise FileException("File %s not exist" % (fileName))
        os.remove(targetFile)
