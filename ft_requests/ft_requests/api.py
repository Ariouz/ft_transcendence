# https://github.com/psf/requests/blob/main/src/requests/api.py

import http.client
import json
from .models import *


def send_request(method, url, body=None, headers=None):
    """
    Raises:
        RequestException
    """
    if headers is None:
        headers = {}
    try:
        host, path = parse_url(url)
        conn = http.client.HTTPSConnection(host)
        conn.request(method=method, url=path, body=body, headers=headers)
    except Exception as e:
        raise RequestException(f"Connection error: {e}")
    return get_response_data(conn)


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
