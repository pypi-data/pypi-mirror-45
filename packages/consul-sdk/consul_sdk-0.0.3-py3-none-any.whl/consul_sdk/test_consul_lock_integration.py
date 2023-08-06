# Third party test lib
import threading
from contextlib import contextmanager

import pytest
from consul_sdk import ConsulLock, UnableToAcquireLock, ConsulClient

import time

from uuid import uuid4


@contextmanager
def lock(lock_key):
    consul_lock = ConsulLock(ConsulClient(), lock_key=lock_key)
    with consul_lock:
        yield


def acquire_lock_and_sleep(key):
    with lock(key):
        time.sleep(2)


@pytest.mark.integration
def test_consul_locking_different_instances():
    key = str(uuid4())
    other_key = str(uuid4())
    t1 = threading.Thread(target=acquire_lock_and_sleep, args=(key,))
    t1.start()

    with pytest.raises(UnableToAcquireLock):
        with lock(key):
            pass

    with lock(other_key):
        pass
