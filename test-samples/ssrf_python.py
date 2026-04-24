import urllib.request


class requests:
    @staticmethod
    def get(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def put(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def patch(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def delete(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def request(*args, **kwargs):
        return args, kwargs

    class Session:
        def get(self, *args, **kwargs):
            return args, kwargs


class httpx:
    class Client:
        def get(self, *args, **kwargs):
            return args, kwargs

    class AsyncClient:
        def post(self, *args, **kwargs):
            return args, kwargs

    @staticmethod
    def request(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def stream(*args, **kwargs):
        return args, kwargs


class treq:
    @staticmethod
    def get(*args, **kwargs):
        return args, kwargs

    @staticmethod
    def post(*args, **kwargs):
        return args, kwargs


class pycurl:
    URL = 10002


class Curl:
    def setopt(self, *args, **kwargs):
        return args, kwargs


class curl_cffi:
    class requests:
        @staticmethod
        def get(*args, **kwargs):
            return args, kwargs


class wget:
    @staticmethod
    def download(*args, **kwargs):
        return args, kwargs


class aiohttp:
    class ClientSession:
        def get(self, *args, **kwargs):
            return args, kwargs

        def post(self, *args, **kwargs):
            return args, kwargs

        def put(self, *args, **kwargs):
            return args, kwargs

        def patch(self, *args, **kwargs):
            return args, kwargs

        def delete(self, *args, **kwargs):
            return args, kwargs

        def request(self, *args, **kwargs):
            return args, kwargs


def vulnerable(user_url):
    requests.get(user_url)
    requests.get("http://169.254.169.254/latest/meta-data/")
    requests.Session().get(user_url)
    urllib.request.urlopen(user_url)
    urllib.request.urlopen("http://localhost/admin")
    httpx.Client().get(user_url)
    httpx.AsyncClient().post(user_url, json={"ping": True})
    aiohttp.ClientSession().get(user_url)
    aiohttp.ClientSession().post(user_url, json={"ping": True})
    requests.put(user_url, data={"key": "value"})
    requests.patch(user_url, data={"key": "value"})
    requests.delete(user_url)
    requests.request("GET", user_url)
    httpx.request("GET", user_url)
    httpx.stream("GET", user_url)
    urllib.request.Request(user_url)
    aiohttp.ClientSession().put(user_url, data={"key": "value"})
    aiohttp.ClientSession().patch(user_url, data={"key": "value"})
    aiohttp.ClientSession().delete(user_url)
    aiohttp.ClientSession().request("GET", user_url)

def false_negative_expansion_ssrf_python(user_url, user_host, httpx, urllib, http):
    urllib.request.urlopen(user_url)
    httpx.get(user_url)
    http.client.HTTPConnection(user_host)


def false_negative_expansion_additional_clients(user_url, user_input, request_url):
    # Vulnerable: user-controlled URLs reach additional HTTP clients.
    treq.get(user_url)
    treq.post(request_url, data={"ping": True})
    Curl().setopt(pycurl.URL, user_input)
    curl_cffi.requests.get(user_url)
    wget.download(user_input)
