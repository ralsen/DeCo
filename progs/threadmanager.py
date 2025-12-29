from threadtools import StoppableThread    
import logging
from threadtools import StoppableThread
import threading

logger = logging.getLogger(__name__)

class ThreadManager:
    def __init__(self):
        self._threads = {}

    def start(self, name: str, target: callable, args: tuple = (), kwargs: dict = None):
        if name in self._threads:
            logger.info(f"Thread '{name}' already running.")
            return

        t = StoppableThread(target=target, name=name, args=args, kwargs=kwargs)
        t.start()
        self._threads[name] = t
        logger.info(f"Thread '{name}' started.")

    def stop(self, name: str):
        thread = self._threads.get(name)
        if thread:
            logger.info(f"Stopping thread '{name}' (externally triggered).")
            thread.stop()
            thread.join(timeout=5)
            if thread.is_alive():
                logger.warning(f"Thread '{name}' did not terminate cleanly..")
            else:
                logger.info(f"Thread '{name}' stopped")
            del self._threads[name]

    def stop_all(self):
        current = threading.current_thread()
        for name, thread in list(self._threads.items()):
            if thread is current:
                continue
            self.stop(name)

    def is_alive(self, name: str) -> bool:
        thread = self._threads.get(name)
        return thread.is_alive() if thread else False

    def get_all(self) -> list:
        return list(self._threads.keys())

    def cleanup_finished(self):
        finished = [name for name, t in self._threads.items() if not t.is_alive()]
        for name in finished:
            logger.info(f"Thread '{name}' has finished.")
            del self._threads[name]