from http import HTTPStatus

import requests


class ConsulClient:
    def __init__(self, host="http://127.0.0.1", port=8500, service_name=None):
        self._host = host
        self._port = port
        self._service_name = service_name

    def acquire_lock(self, key, session_id):
        payload = {"acquire": session_id}
        return self._put_key(key, payload)

    def release_lock(self, key, session_id):
        payload = {"release": session_id}
        return self._put_key(key, payload)

    def get_key(self, key):
        response = requests.get(f"{self._host}:{self._port}/v1/kv/{key}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        assert response.status_code == HTTPStatus.OK
        return response.json()[0]

    def create_session(
        self, ttl_in_secs: int, lock_delay_in_secs: int = 15, behavior="release"
    ):
        payload = {
            "LockDelay": f"{lock_delay_in_secs}s",
            "Name": self._service_name,
            "Node": None,
            "Checks": [],
            "Behavior": behavior,
            "TTL": f"{ttl_in_secs}s",
        }

        response = requests.put(
            f"{self._host}:{self._port}/v1/session/create", json=payload
        )

        assert response.status_code == HTTPStatus.OK
        return response.json()["ID"]

    def renew_session(self, session_id):
        response = requests.put(
            f"{self._host}:{self._port}/v1/session/renew/{session_id}"
        )

        assert response.status_code == HTTPStatus.OK

    def get_session(self, session_id):
        response = requests.get(
            f"{self._host}:{self._port}/v1/session/info/{session_id}"
        )

        assert response.status_code == HTTPStatus.OK

        data = response.json()
        if len(data) == 0:
            return None

        session = data[0]
        return session["ID"]

    def _put_key(self, key, payload):
        response = requests.put(f"{self._host}:{self._port}/v1/kv/{key}", json=payload)

        assert response.status_code == HTTPStatus.OK

        return response.json()
