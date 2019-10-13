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