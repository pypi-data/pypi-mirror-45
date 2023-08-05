from ..settings import DEFAULT_TIMEOUT, POSTS_SUFFIX
from .make_url import make_url
from .make_request import make_request


def do_get_posts(url, timeout=DEFAULT_TIMEOUT):
    url = make_url(url, POSTS_SUFFIX)
    res = make_request("get", url, timeout)
    return res
