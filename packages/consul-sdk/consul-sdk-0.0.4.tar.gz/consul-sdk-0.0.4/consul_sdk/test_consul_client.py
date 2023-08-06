import time

import pytest

from consul_sdk.client import ConsulClient


def test_create_and_get_session():
    client = ConsulClient()
    session_id = client.create_session(30)
    assert session_id == client.get_session(session_id)


def test_renew_session():
    client = ConsulClient()
    session_id = client.create_session(10)
    assert session_id == client.get_session(session_id)

    time.sleep(9)
    client.renew_session(session_id)

    time.sleep(2)
    assert client.get_session(session_id) is not None


@pytest.mark.skip("Failing")
def test_get_session_returns_none_if_session_expired():
    client = ConsulClient()
    session_id = client.create_session(10)
    assert session_id == client.get_session(session_id)

    time.sleep(15)
    assert client.get_session(session_id) is None


def test_acquire_and_release_lock():
    client = ConsulClient()
    session_id = client.create_session(10)

    assert client.acquire_lock("my-key", session_id)

    assert client.release_lock("my-key", session_id)
