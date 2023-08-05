import base64


def get_authentication_header(username, password):
    decoded = "{}:{}".format(username, password)
    encoded = base64.b64encode(bytes(decoded, encoding="utf-8"))
    return {"Authentication": "Basic {}".format(encoded)}
