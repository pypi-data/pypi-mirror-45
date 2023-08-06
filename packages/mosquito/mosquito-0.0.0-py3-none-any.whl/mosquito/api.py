# Standard library modules.
from contextlib import contextmanager

# Third party modules.

# Local modules
from mosquito.utils import MosquitoError
from mosquito.session_manager import SessionManager
from mosquito.request_scheduler import RequestScheduler

# Globals and constants variables.
ATTRIBUTE_REGISTRY = dict()


def available_attributes():
    return sorted(getattr(SessionManager, '__attrs__'))


def register_attributes(**kwargs):
    for attr, value in kwargs.items():
        if attr not in available_attributes():
            raise MosquitoError(f'unknown attribute "{attr}"')

        ATTRIBUTE_REGISTRY[attr] = value


def attribute(attr):
    def attribute_decorator(value):
        register_attributes(**{attr: value})

        return value

    return attribute_decorator


@contextmanager
def swarm(max_attempts=3, repeat_on=None):
    session_manager = SessionManager(**ATTRIBUTE_REGISTRY)

    try:
        session_manager.open()
        yield RequestScheduler(session_manager, max_attempts, repeat_on)

    finally:
        session_manager.close()


def monitor():
    return SessionManager.monitor
