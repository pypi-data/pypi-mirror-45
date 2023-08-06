#!/usr/bin/env python3
from functools import wraps
from itertools import count

# Third party modules.

# Local modules
from mosquito.utils import MosquitoError
from mosquito.session_manager import MosquitoSession

# Globals and constants variables.


class RequestScheduler:
    def __init__(self, session_manager, max_attempts=1, repeat_on=None):
        self._session_manager = session_manager
        self._max_attempts = max_attempts
        self._repeat_on = repeat_on or ()

    def _request(self, request_method, url, **kwargs):
        _range = range(1, self._max_attempts + 1) if self._max_attempts else count()

        for i in _range:
            with self._session_manager.session() as session:
                response = request_method(session, url, **kwargs)

                status_code = response.status_code

                # return response on success
                if status_code == 200:
                    return response

                # repeat if status code is whitelisted
                elif status_code in self._repeat_on:
                    continue

                raise MosquitoError(f'request failed with code {status_code} on {i} attempt')

        raise MosquitoError(f'request failed after {self._max_attempts} attempts')

    @wraps(MosquitoSession.get)
    def get(self, *args, **kwargs):
        return self._request(MosquitoSession.get, *args, **kwargs)

    @wraps(MosquitoSession.options)
    def options(self, *args, **kwargs):
        return self._request(MosquitoSession.options, *args, **kwargs)

    @wraps(MosquitoSession.head)
    def head(self, *args, **kwargs):
        return self._request(MosquitoSession.head, *args, **kwargs)

    @wraps(MosquitoSession.post)
    def post(self, *args, **kwargs):
        return self._request(MosquitoSession.post, *args, **kwargs)

    @wraps(MosquitoSession.put)
    def put(self, *args, **kwargs):
        return self._request(MosquitoSession.put, *args, **kwargs)

    @wraps(MosquitoSession.patch)
    def patch(self, *args, **kwargs):
        return self._request(MosquitoSession.patch, *args, **kwargs)

    @wraps(MosquitoSession.delete)
    def delete(self, *args, **kwargs):
        return self._request(MosquitoSession.delete, *args, **kwargs)
