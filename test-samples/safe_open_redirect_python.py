from urllib.parse import urlparse


def safe_redirect(target):
    allowed_hosts = {'example.com'}
    parsed = urlparse(target)
    if parsed.netloc and parsed.netloc not in allowed_hosts:
        raise ValueError('invalid redirect')
    return target


def safe(user_url):
    validated = safe_redirect(user_url)
    return {"url": validated, "status": 302}


def safe_django():
    return {"redirect": "/dashboard", "status": 302}


def safe_validated_redirect(user_url):
    validated = safe_redirect(user_url)
    return {"url": validated, "status": 302}
