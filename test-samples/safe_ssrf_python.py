from urllib.parse import urlparse


class http_client:
    @staticmethod
    def get(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def put(*args, **kwargs):
        return args, kwargs


class httpx:
    class Client:
        def __init__(self, timeout):
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, *args, **kwargs):
            return args, kwargs

        def stream(self, *args, **kwargs):
            return args, kwargs


ALLOWED_HOSTS = {"api.example.com", "files.example.com"}


def is_safe_url(url):
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS


def fetch_profile(url):
    if not is_safe_url(url):
        raise ValueError("untrusted url")

    http_client.get(url, timeout=3)
    http_client.put(url, timeout=3)
    with httpx.Client(timeout=3) as client:
        return client.get(url), client.stream("GET", url)
