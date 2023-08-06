# Standard library modules.
from threading import Lock
from functools import wraps
from time import time, sleep
from collections import Counter
from contextlib import contextmanager
from queue import PriorityQueue, Empty

# Third party modules.
import requests

# Local modules
from mosquito.utils import logger, MosquitoError, SingletonContext

# Globals and constants variables.


class Monitor:
    def __init__(self):
        self._lock = Lock()
        self.status_codes = Counter()

    def __str__(self):
        return f'<{self.__class__.__name__}(status_codes={self.status_codes})>'

    def update(self, response):
        with self._lock:
            self.status_codes.update([response.status_code])


class MosquitoSession(requests.Session):
    def __init__(self, sid, monitor, headers=None, auth=None, proxies=None, hooks=None, params=None,
                 stream=None, verify=None, prefetch=None, cert=None, max_redirects=None,
                 trust_env=None, cookies=None, adapters=None):

        super().__init__()

        self._sid = sid
        self.monitor = monitor or Monitor()

        if headers:
            self.headers.update(headers)
        if auth:
            self.auth = auth
        if proxies:
            self.proxies.update(proxies)
        if hooks:
            self.hooks.update(hooks)
        if params:
            self.params.update(params)
        if stream is not None:
            self.stream = bool(stream)
        if verify is not None:
            self.verify = bool(verify)
        if cert is not None:
            self.cert = cert
        if prefetch is not None:
            self.prefetch = prefetch
        if max_redirects is not None:
            self.max_redirects = int(max_redirects)
        if trust_env is not None:
            self.trust_env = bool(trust_env)
        if cookies:
            self.cookies.update(cookies)
        if adapters:
            self.adapters.update(adapters)

    def __str__(self):
        return f'<{self.__class__.__name__}(id={self.id})>'

    @property
    def id(self):
        return self._sid

    @wraps(requests.Session.request)
    def request(self, method, url, *args, **kwargs):
        logger.debug(f'{self}: {method} {url}')
        response = super().request(method, url, *args, **kwargs)

        self.monitor.update(response)
        return response


class SessionManager(SingletonContext):
    __attrs__ = ['on_init', 'delay', 'require', *MosquitoSession.__attrs__]
    monitor = Monitor()

    def __init__(self, delay=0., on_init=None, require=None, **session_attributes):
        super().__init__(
            _delay=delay,
            _on_init=on_init,
            _require=require,
            _session_attributes=session_attributes,
            _lock=Lock(),
            _sessions=PriorityQueue()
        )

    def __len__(self):
        with self._lock:
            return self._sessions.qsize()

    def _put_session(self, session):
        self._sessions.put((time(), session))

    def _get_session(self, timeout):
        time_stamp, session = self._sessions.get(block=True, timeout=timeout)

        sleep(max(0, self.evaluate(self._delay) - (time() - time_stamp)))

        return session

    @contextmanager
    def session(self, timeout=None):
        session = self._get_session(timeout)

        try:
            yield session

        finally:
            self._put_session(session)

    @staticmethod
    def evaluate(value, *args, **kwargs):
        if callable(value):
            value = value(*args, **kwargs)

        try:
            return list(value)

        except TypeError:
            return value

    def on_open(self):
        session_attributes = {
            attr: self.evaluate(value) for attr, value in self._session_attributes.items()
            if attr in MosquitoSession.__attrs__
        }

        for attribute in self.evaluate(self._require) or ():
            if attribute not in MosquitoSession.__attrs__:
                raise AttributeError(f'unknown attribute "{attribute}"')

            if attribute not in session_attributes:
                raise MosquitoError(f'requirement "{attribute}" is not fulfilled')

        if session_attributes:
            attributes, values = zip(*session_attributes.items())

            for i, v in enumerate(zip(*values)):
                session = MosquitoSession(sid=i, monitor=self.monitor, **dict(zip(attributes, v)))

                if self._on_init:
                    self._on_init(session)

                self._put_session(session)

        else:
            session = MosquitoSession(sid=0, monitor=self.monitor)

            if self._on_init:
                self._on_init(session)

            self._put_session(session)

        logger.debug(f'opened manager for {len(self)} sessions')

    def on_close(self):
        try:
            while True:
                _, session = self._sessions.get(block=False)
                session.close()

        except Empty:
            pass

        logger.debug(f'closed manager successfully ({len(self)} sessions remain)')
