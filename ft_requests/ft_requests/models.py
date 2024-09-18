# https://github.com/psf/requests/blob/main/src/requests/models.py

import http.client
import json
from .exceptions import *


class Response:
    def __init__(self, status, data):
        self.status = status
        self.data = data
        self._json = None

    @property
    def status_code(self):
        return self.status

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

    def __str__(self):
        return f"Response(status_code={self.status}, data={self.data[:100]})"

    def __repr__(self):
        return self.__str__()
