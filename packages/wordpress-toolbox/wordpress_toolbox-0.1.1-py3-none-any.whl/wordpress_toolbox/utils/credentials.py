import json
import os
import io

from ..settings import DEFAULT_CREDENTIALS_FILE_NAME
from ..exceptions import (
    CredentialsFileMissingException,
    CredentialsNotFoundException
)


def set_credentials(
    url,
    username,
    password,
    credentials_file_name=DEFAULT_CREDENTIALS_FILE_NAME
):
    path = os.path.join(os.path.expanduser("~"), credentials_file_name)
    data = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as old_file:
            data = json.loads(old_file.read())
    with open(path, "w", encoding="utf-8") as new_file:
        data[url] = {
            "username": username,
            "password": password,
        }
        new_file.write(json.dumps(data))


def get_credentials(
    url,
    credentials_file_name=DEFAULT_CREDENTIALS_FILE_NAME
):
    path = os.path.join(os.path.expanduser("~"), credentials_file_name)
    if not os.path.isfile(path):
        raise CredentialsFileMissingException(
            "There is no credentials file found."
        )
    with open(path, encoding="utf-8") as f:
        data = json.loads(f.read())
        if url not in data:
            raise CredentialsNotFoundException(
                "There are no credentials for that url."
            )
        credentials = data[url]
        return (credentials["username"], credentials["password"])

