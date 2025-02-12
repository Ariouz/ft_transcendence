# https://github.com/psf/requests/blob/main/src/requests/api.py

import http.client
import json
from .models import *
from .utils import *
from http.cookies import SimpleCookie

COOKIE_STORAGE = {}


def send_request(method, url, body=None, headers=None):
    """
    Raises:
        RequestException
    """
    if headers is None:
        headers = {}
    try:
        host, path, port, scheme = parse_url(url)

        if host in COOKIE_STORAGE:
            headers["Cookie"] = COOKIE_STORAGE[host]

        conn = http.client.HTTPSConnection(host, port=port) if scheme == "https" else http.client.HTTPConnection(host, port=port)
        conn.request(method=method, url=path, body=body, headers=headers)

        response = conn.getresponse()
        response_data = get_response_data(response)
        conn.close()

        set_cookie_header = response.getheader("Set-Cookie")
        if set_cookie_header:
            store_cookies(host, set_cookie_header)

    except Exception as e:
        raise RequestException(f"Connection error: {e}")
    return response_data


def get(url, headers=None):
    """
    Raises:
        RequestException
    """
    return send_request("GET", url, headers=headers)


def post(url, data=None, headers=None):
    """
    Raises:
        RequestException
    """
    if headers is None:
        headers = {"Content-Type": "application/json"}
    if data and isinstance(data, dict):
        data = json.dumps(data)
    return send_request("POST", url, data, headers)


def delete(url, headers=None):
    """
    Raises:
        RequestException
    """
    return send_request("DELETE", url, headers=headers)


def store_cookies(host, set_cookie_header):
    """
    Parses 'Set-Cookie' header and stores cookies per domain.
    """
    cookie = SimpleCookie()
    cookie.load(set_cookie_header)

    cookies = "; ".join([f"{key}={morsel.value}" for key, morsel in cookie.items()])
    COOKIE_STORAGE[host] = cookies
