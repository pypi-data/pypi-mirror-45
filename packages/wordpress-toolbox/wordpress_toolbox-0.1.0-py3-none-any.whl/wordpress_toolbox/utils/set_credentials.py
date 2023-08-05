import os
import json

from ..settings import DEFAULT_CREDENTIALS_FILE_NAME


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
