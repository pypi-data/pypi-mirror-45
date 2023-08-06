import threading
from datetime import datetime, timedelta

from consul_sdk.client import ConsulClient


class UnableToAcquireLock(Exception):
    pass


thread_lock = threading.Lock()


class ConsulLock:
    _session_id = None
    _session_expiry = None

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
        return self.client.acquire_lock(
            key=self.lock_key, session_id=self._get_session_id()
        )

    def _refresh_or_create_session(self):
        if (
            self._get_session_id() is None
            or self.client.get_session(self._get_session_id()) is None
        ):
            self._set_session_id(self.client.create_session(ttl_in_secs=self.ttl))
            self._set_session_expiry(datetime.now() + timedelta(seconds=self.ttl))

        if self._get_session_expiry() < (
            datetime.now() + timedelta(seconds=self.ttl / 2)
        ):
            self.client.renew_session(self._session_id)

    def _release(self):
        self.client.release_lock(key=self.lock_key, session_id=self._get_session_id())

    @classmethod
    def _get_session_id(cls):
        return cls._session_id

    @classmethod
    def _get_session_expiry(cls):
        return cls._session_expiry

    @classmethod
    def _set_session_id(cls, session_id):
        cls._session_id = session_id

    @classmethod
    def _set_session_expiry(cls, expiry):
        cls._session_expiry = expiry
