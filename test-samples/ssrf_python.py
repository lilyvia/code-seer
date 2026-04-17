import urllib.request


class requests:
    @staticmethod
    def get(*args, **kwargs):
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


class aiohttp:
    class ClientSession:
        def get(self, *args, **kwargs):
            return args, kwargs

        def post(self, *args, **kwargs):
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
