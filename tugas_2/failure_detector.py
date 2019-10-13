import datetime
import threading
import time
import typing

class Listener:
    def __init__(self, host: str, deltaTime: datetime.timedelta, onChange = None, onRecover = None):
        self.sequence = 0
        self.host = host
        self.seq = 0
        self.deltaTime = deltaTime
        self.onChange = onChange
        self.onRecover = onRecover
        self.status = "ONLINE"
        self.lastBeat = datetime.datetime.now()

    def Refresh(self, sequence):
        self.lastBeat = datetime.datetime.now()
        if self.sequence > sequence:
            if self.onRecover is not None:
                self.onRecover()
        self.sequence = sequence + 1

    
    def Check(self):
        referenceTime = datetime.datetime.now().__add__(-self.deltaTime * 2)
        isStatusChange = False
        if self.lastBeat.timestamp() < referenceTime.timestamp():
            if self.status != "OFFLINE":
                self.status = "OFFLINE"
                isStatusChange = True
        else:
            if self.status != "ONLINE":
                self.status = "ONLINE"
                isStatusChange = True

        if isStatusChange:
            if self.onChange is not None:
                self.onChange(self.status)
    
    def GetStatus(self):
        return self.status

class FailureDetector:
    def __init__(self, deltaTime: datetime.timedelta):
        self.listener: typing.Dict[str, Listener] = dict()
        self.deltaTime = deltaTime
        self.sequence = 0

    def Broadcast(self, targets):
        for target in targets:
            self.Notify(target, self.sequence)
        self.sequence += 1

    def AddListener(self, host, onChange=None, onRecover=None):
        self.listener[host] = Listener(host, self.deltaTime, onChange, onRecover)

    def Notify(self, host, sequence):
        raise Exception("Not implemented")

    def Ping(self, host):
        raise Exception("Not implemented")

    def Ack(self):
        return "OK"

    def OnNotify(self, host, sequence):
        self.listener[host].Refresh(sequence)

    def __run__daemon__(self):
        thread = threading.Thread(target=self.__daemon__)
        thread.daemon = True
        thread.start()

    def __daemon__(self):
        sleepTime = 1.0
        time.sleep(sleepTime)
        while True:
            time.sleep(sleepTime)
            for listener in self.listener:
                self.listener[listener].Check()
