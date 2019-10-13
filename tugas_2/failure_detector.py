import datetime
import threading
import time
import typing

class Listener:
    def __init__(self, host: str, deltaTime: datetime.timedelta, onChange = None):
        self.host = host
        self.seq = 0
        self.deltaTime = deltaTime
        self.onChange = onChange
        self.status = "OFFLINE"
        self.Refresh()

    def Refresh(self):
        self.lastBeat = datetime.datetime.now()
    
    def Check(self):
        referenceTime = datetime.datetime.now().__add__(-self.deltaTime * 2)
        isStatusChange = False
        if self.lastBeat.timestamp() < referenceTime:
            if self.status != "OFFLINE":
                self.status = "OFFLINE"
                isStatusChange = True
        else:
            if self.status != "ONLINE":
                self.status = "ONLINE"
                isStatusChange = True

        if isStatusChange:
            if self.onChange is not None:
                self.onChange(self.host, self.status)
    
    def GetStatus(self):
        return self.status

class FailureDetector:
    def __init__(self, deltaTime: datetime.timedelta):
        self.listener: typing.Dict[str, Listener] = dict()
        self.deltaTime = deltaTime

    def Broadcast(self, targets):
        for target in targets:
            self.Notify(target)

    def AddListener(self, host, onChange=None):
        self.listener[host] = Listener(host, self.deltaTime, onChange)

    def Notify(self, host):
        raise Exception("Not implemented")

    def Ping(self, host):
        raise Exception("Not implemented")

    def Ack(self):
        return "OK"

    def OnNotify(self, host):
        self.listener[host].Refresh()

    def __run__daemon__(self):
        thread = threading.Thread(target=self.__daemon__)
        thread.daemon = True
        thread.start()

    def __daemon__(self):
        sleepTime = self.deltaTime.total_seconds()
        time.sleep(sleepTime)
        while True:
            time.sleep(sleepTime)
            for listener in self.listener.items():
                listener.Check()
