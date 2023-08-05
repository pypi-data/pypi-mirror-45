import requests
import json
import os

from .settings import DEFAULT_HEADERS


def make_request(method, url, timeout, data={}, headers={}):
    try:
        fn = getattr(requests, method)
        if method == "post":
            res = fn(
                url,
                timeout=timeout,
                data=json.dumps(data),
                headers=DEFAULT_HEADERS.update(headers)
            )
        else:
            res = fn(url, timeout=timeout)
    except requests.ConnectionError:
        return "{}: Timed out after {} seconds.".format(url, timeout)
    status_code = res.status_code
    if status_code != 200:
        return "{}: {} - {}".format(url, status_code, res.message)
    else:
        return res.json()


def make_url(url, suffix, *args):
    if not url.endswith(suffix):
        url = "/".join([ url, suffix ])
    url = "/".join([ url ] + list(args))
    return url
