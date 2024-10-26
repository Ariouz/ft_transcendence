from .models import Response
from .exceptions import RequestException
import http.client
from urllib.parse import urlparse


DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443


def parse_url(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    host = parsed_url.hostname
    path = parsed_url.path or "/"
    if parsed_url.query:
        path += "?" + parsed_url.query
    if scheme == "https":
        port = parsed_url.port or DEFAULT_HTTPS_PORT
    elif scheme == "http":
        port = parsed_url.port or DEFAULT_HTTP_PORT
    port = parsed_url.port
    return host, path, port, scheme


def get_response_data(conn):
    try:
        response = conn.getresponse()
        content_type = response.getheader('Content-Type')
        if 'text' in content_type or 'application/json' in content_type:
            data = response.read().decode("utf-8")
        else:
            data = response.read()
        conn.close()
        return Response(response.status, data)
    except http.client.HTTPException as e:
        raise RequestException(f"Connection error: {e}")
