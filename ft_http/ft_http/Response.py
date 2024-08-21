import http.client
import json
from urllib.parse import urlparse
from .exceptions import *

class Response:
    def __init__(self, status, data):
        self.status = status
        self.data = data
        self._json = None

    def raise_for_status(self):
        if not (200 <= self.status < 300):
            raise http.client.HTTPException(f"HTTP Error: {self.status}")

    def json(self):
        if self._json is None:
            try:
                self._json = json.loads(self.data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON response")
        return self._json


def get_response_data(conn):
    try:
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()
        return Response(response.status, data)
    except (http.client.HTTPException) as e:
        raise RequestException(f"Connection error: {e}")



def parse_url(url):
    urlParsed = urlparse(url)
    host, path = urlParsed.hostname, urlParsed.path
    return host, path

