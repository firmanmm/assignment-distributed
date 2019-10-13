import Pyro4
import failure_detector
import datetime

class PyroFailureDetector(failure_detector.FailureDetector):
    def __init__(self, identifier, deltaTime: datetime.timedelta):
        super().__init__(deltaTime)
        self.identifier = identifier

    def Notify(self, host):
        try:
            proxy = Pyro4.Proxy(host)
            proxy.OnNotify(self.identifier)
        except Exception as e:
            print(e)
            pass

    def Ping(self, host):
        try:
            proxy = Pyro4.Proxy(host)
            res = proxy.Ack()
            return res == "OK"
        except:
            return False