import server
import datetime

class Listener:
    def __init__(self, identifier):
        self.identifier = identifier

    def OnRecover(self):
        print("Service %s is recovering from failure" % (self.identifier))

    def OnChange(self, status):
        if status == "ONLINE":
            print("Service UP %s" % (self.identifier))
        else:
            print("Service DOWN %s" % (self.identifier))
    
    def GetIdentifier(self):
        return self.identifier
    

if __name__ == '__main__':
    pyroServer = server.Server("localhost", 7777)
    failureDetectorServer = server.FailureDetectorServer(datetime.timedelta(seconds=5), identifier="FailureDetectorServer")
    fileServer1 = Listener("FS1-FileServer")
    fileServer2 = Listener("FS2-FileServer")
    failureDetectorServer.AddListener(fileServer1.GetIdentifier(), fileServer1.OnChange, fileServer1.OnRecover)
    failureDetectorServer.AddListener(fileServer2.GetIdentifier(), fileServer2.OnChange, fileServer2.OnRecover)
    pyroServer.Start([failureDetectorServer])