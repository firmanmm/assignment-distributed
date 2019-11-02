import threading

class Sync:

    def __init__(self):
        self.mapLock = dict()

    def AcquireLock(self, key: str):
        lock = None
        if key in self.mapLock:
            lock = self.mapLock[key]
        else:
            lock = threading.Lock()
            self.mapLock[key] = lock
        lock.acquire(timeout=5)
    
    def ReleaseLock(self, key: str):
        if key in self.mapLock:
            self.mapLock[key].release()