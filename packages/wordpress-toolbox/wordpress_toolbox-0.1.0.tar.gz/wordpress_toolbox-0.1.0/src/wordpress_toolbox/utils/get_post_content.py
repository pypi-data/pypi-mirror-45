from .make_url import make_url
from .make_request import make_request
from ..settings import POSTS_SUFFIX


def get_post_content(url, number=0):
    url = make_url(url, POSTS_SUFFIX)
    res = make_request("get", url)
    return res[number]["content"]["rendered"]
