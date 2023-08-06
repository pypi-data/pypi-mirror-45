import threading
from datetime import datetime, timedelta


from consul_sdk.client import ConsulClient


class UnableToAcquireLock(Exception):
    pass


thread_lock = threading.Lock()


class ConsulLock:
    SHORT_TTL = 30
    LONG_TTL = 300  # 5 mins

    def __init__(self, client: ConsulClient, lock_key: str, ttl=SHORT_TTL):
        self.client: ConsulClient = client
        self.lock_key = lock_key
        self.ttl = ttl

    def __enter__(self):
        thread_lock.acquire(blocking=True)
        try:
            self._refresh_or_create_session()
        except Exception as e:
            thread_lock.release()
            raise e

        thread_lock.release()
        if not self._acquire():
            raise UnableToAcquireLock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._release()
        if exc_type:
            raise exc_type(exc_val, exc_tb)

    def _acquire(self):
        return self.client.acquire_lock(key=self.lock_key, session_id=_get_session_id())

    def _refresh_or_create_session(self):
        if (
            _get_session_id() is None
            or self.client.get_session(_get_session_id()) is None
        ):
            _set_session_id(self.client.create_session(ttl_in_secs=self.ttl))
            _set_session_expiry(datetime.now() + timedelta(seconds=self.ttl))

        if _get_session_expiry() < (datetime.now() + timedelta(seconds=self.ttl / 2)):
            self.client.renew_session(_get_session_id())

    def _release(self):
        self.client.release_lock(key=self.lock_key, session_id=_get_session_id())


_data = threading.local()


def _get_session_id():
    if hasattr(_data, "session_id"):
        return _data.session_id
    else:
        return None


def _set_session_id(session_id):
    global _data
    _data.session_id = session_id


def _get_session_expiry() -> datetime:
    if hasattr(_data, "session_expiry"):
        return _data.session_expiry
    else:
        return None


def _set_session_expiry(session_expiry):
    global _data
    _data.session_expiry = session_expiry
