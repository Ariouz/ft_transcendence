import http.client
import json
from urllib.parse import urlencode, urlparse


def get_response_data(conn):
    response = conn.getresponse()
    data = response.read().decode("utf-8")
    conn.close()
    return response.status, data

def parse_url(url):
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    path = parsed_url.path
    return host, path


def http_get(url, headers=None, params=None):
    host, path = parse_url(url)
    conn = http.client.HTTPSConnection(host)
    if params:
        path = f"{path}?{urlencode(params)}"

    if headers is None:
        headers = {}

    conn.request("GET", path, headers=headers)
    return get_response_data(conn)


def http_post(url, body=None, headers=None):
    host, path = parse_url(url)
    conn = http.client.HTTPSConnection(host)

    if headers is None:
        headers = {"Content-Type": "application/json"}

    if body and isinstance(body, dict):
        body = json.dumps(body)

    conn.request("POST", path, body, headers)
    return get_response_data(conn)


def http_delete(url, headers=None):
    host, path = parse_url(url)
    conn = http.client.HTTPSConnection(host)

    if headers is None:
        headers = {}

    conn.request("DELETE", path, headers=headers)
    return get_response_data(conn)
