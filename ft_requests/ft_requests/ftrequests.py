import http.client
import json
from .Response import *

class ftrequests:
    @staticmethod
    def get(url, headers=None):
        host, path = parse_url(url)
        conn = http.client.HTTPSConnection(host)

        if headers is None:
            headers = {}

        conn.request("GET", path, headers=headers)
        return get_response_data(conn)


    @staticmethod
    def post(url, data=None, headers=None):
        host, path = parse_url(url)
        conn = http.client.HTTPSConnection(host)

        if headers is None:
            headers = {"Content-Type": "application/json"}

        if data and isinstance(data, dict):
            data = json.dumps(data)

        conn.request("POST", path, data, headers)
        return get_response_data(conn)


    @staticmethod
    def delete(url, headers=None):
        host, path = parse_url(url)
        conn = http.client.HTTPSConnection(host)

        if headers is None:
            headers = {}

        conn.request("DELETE", path, headers=headers)
        return get_response_data(conn)

