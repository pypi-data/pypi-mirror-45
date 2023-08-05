POSTS_SUFFIX = "wp-json/wp/v2/posts"

DEFAULT_TIMEOUT = 10.0

DEFAULT_HEADERS = {
    "Content-Type": "application/json"
}

HTTP_SCHEMES = ("http://", "https://",)

DEFAULT_CREDENTIALS_FILE_NAME = "wordpress_toolbox_credentials.json"

HTTP_METHODS_ALLOWED = (
    "get", "post", "put", "delete", "options", "head",
)
