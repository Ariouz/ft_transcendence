# https://github.com/psf/requests/blob/main/src/requests/api.py

import http.client
import json
from .models import *
from .utils import *


def send_request(method, url, body=None, headers=None):
    """
    Raises:
        RequestException
    """
    if headers is None:
        headers = {}
    try:
        host, path, port, scheme = parse_url(url)
        conn = None
        if scheme == "https":
            conn = http.client.HTTPSConnection(host, port=port)
        elif scheme == "http":
            conn = http.client.HTTPConnection(host, port=port)
        else:
            raise RequestException(f"Unsupported URL scheme: {scheme}")
        conn.request(method=method, url=path, body=body, headers=headers)
        response_data = get_response_data(conn)
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
