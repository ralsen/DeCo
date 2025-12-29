import threading

class StoppableThread(threading.Thread):
    def __init__(self, target: callable, name=None, args=(), kwargs=None):
        super().__init__(name=name)
        self._stop_event = threading.Event()
        self._target = target
        self._args = args
        self._kwargs = kwargs or {}
        
    def run(self):
        self._target(self._stop_event, *self._args, **self._kwargs)

    def stop(self):
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()