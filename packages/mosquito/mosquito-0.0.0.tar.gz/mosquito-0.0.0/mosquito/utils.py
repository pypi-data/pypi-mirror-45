# Standard library modules.
import abc
import sys
import queue
import logging
from threading import Lock
from functools import wraps

# Third party modules.
from tqdm.autonotebook import tqdm

# Local modules

# Globals and constants variables.
FORMAT_STRING = '%(asctime)s %(threadName)s %(levelname)s:\t%(message)s'

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(FORMAT_STRING))

logger = logging.getLogger('mosquito')
logger.addHandler(handler)


class MosquitoError(Exception):
    """mosquito specific error"""


def monitor_queue(qclass):
    class _MonitorQueue(qclass):
        @wraps(qclass.__init__)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._monitor = None

        def __enter__(self):
            self._monitor = tqdm(desc='queue', unit=' tasks')
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._monitor.close()
            self._monitor = None

        @wraps(qclass.task_done)
        def task_done(self):
            if self._monitor is not None:
                self._monitor.update(1)
            super().task_done()

    _MonitorQueue.__name__ = qclass.__name__
    _MonitorQueue.__doc__ = qclass.__doc__

    return _MonitorQueue


@monitor_queue
class MonitoredQueue(queue.Queue):
    """MonitorQueue"""


class SingletonMeta(type):
    def __init__(cls, name, bases, dct):
        super(SingletonMeta, cls).__init__(name, bases, dct)

        _new = cls.__new__

        @wraps(cls.__new__)
        def _new_wrapper(kls, *_, **__):
            if kls.instance is None:
                kls.instance = _new(kls)
            return kls.instance

        cls.instance = None
        cls.__new__ = classmethod(_new_wrapper)


class AbstractSingletonMeta(abc.ABCMeta, SingletonMeta):
    """Mixin for `abc.ABCMeta` and `SingletonMeta`"""


class SingletonContext(metaclass=AbstractSingletonMeta):
    __lock = Lock()
    __ref_counter = 0

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, getattr(self, key, value))

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def count(self):
        with self.__lock:
            return self.__ref_counter

    @abc.abstractmethod
    def on_open(self):
        raise NotImplemented

    def on_close(self):
        pass

    def open(self):
        with self.__lock:
            try:
                if self.__ref_counter == 0:
                    self.on_open()

            finally:
                self.__ref_counter += 1

        return self

    def close(self):
        with self.__lock:
            self.__ref_counter -= 1

            if self.__ref_counter <= 0:
                self.on_close()
