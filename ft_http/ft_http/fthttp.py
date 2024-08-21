import http.client
import json
from Response import *

class fthttp:
    @staticmethod
    def get(url, headers=None):
        host, path = parse_url(url)
        conn = http.client.HTTPSConnection(host)

        if headers is None:
            headers = {}

        conn.request("GET", path, headers=headers)
        return get_response_data(conn)


    @staticmethod
    def post(url, body=None, headers=None):
        host, path = parse_url(url)
        conn = http.client.HTTPSConnection(host)

        if headers is None:
            headers = {"Content-Type": "application/json"}

        if body and isinstance(body, dict):
            body = json.dumps(body)

        conn.request("POST", path, body, headers)
        return get_response_data(conn)


    @staticmethod
    def delete(url, headers=None):
        host, path = parse_url(url)
        conn = http.client.HTTPSConnection(host)

        if headers is None:
            headers = {}

        conn.request("DELETE", path, headers=headers)
        return get_response_data(conn)

