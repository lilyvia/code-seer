import requests
import urllib.request


def vulnerable(user_url):
    requests.get(user_url)
    requests.get("http://169.254.169.254/latest/meta-data/")
    urllib.request.urlopen(user_url)
