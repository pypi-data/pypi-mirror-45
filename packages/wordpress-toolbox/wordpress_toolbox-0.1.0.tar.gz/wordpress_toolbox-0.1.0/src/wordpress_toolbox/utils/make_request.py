import requests
import json

from ..settings import (
    DEFAULT_TIMEOUT,
    DEFAULT_HEADERS,
    HTTP_METHODS_ALLOWED,
)
from ..exceptions import (
    RequestMethodIncorrectException,
    RequestTimeoutException,
    RequestFailureException,
)


def make_request(
    method,
    url,
    params={},
    data={},
    headers={},
    timeout=DEFAULT_TIMEOUT,
):
    method = method.lower()
    try:
        fn = getattr(requests, method)
    except AttributeError:
        raise RequestMethodIncorrectException(
            "Method must be one of: {}".format(
                ", ".join(list(HTTP_METHODS_ALLOWED))
            )
        )
    try:
        if method in ("get", "options", "head",):
            response = fn(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )
        else:
            response = fn(
                url,
                params=params,
                data=json.dumps(data),
                headers=DEFAULT_HEADERS.update(headers),
                timeout=timeout,
            )
        status_code = response.status_code
        content = response.json()
        if status_code != 200:
            raise RequestFailureException(
                "{}: {} - {}".format(url, status_code, content["message"])
            )
        return content
    except requests.ConnectionError:
        raise RequestTimeoutException(
            "{}: Timed out after {} seconds.".format(url, timeout)
        )
