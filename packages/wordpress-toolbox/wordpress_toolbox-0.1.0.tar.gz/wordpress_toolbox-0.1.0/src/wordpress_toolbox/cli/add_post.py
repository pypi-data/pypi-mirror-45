import click
from slugify import slugify

from ..utils import (
    make_url,
    make_request,
    create_post_content,
    get_credentials,
    get_authentication_header,
)
from ..settings import POSTS_SUFFIX


@click.command()
@click.option("--title")
@click.option("--markup")
@click.pass_obj
def add_post(options, title, markup):
    # credentials = get_credentials(options.url)
    # headers = get_authentication_header(**credentials)
    headers = {}
    url = make_url(options.url, POSTS_SUFFIX)
    timeout = options.timeout
    data = make_request(
        method="get",
        url=url,
        timeout=timeout,
    )[0]
    slug = slugify(title)
    data["content"]["rendered"] = create_post_content(options.url, markup)
    data["title"]["rendered"] = title,
    data["id"] = int(data["id"]) + 1
    data["status"] = "draft"
    data["slug"] = slug
    data["link"] = "/".join([options.url, slug])
    click.echo(make_request(
        method="post",
        url=url,
        data=data,
        headers=headers,
        timeout=timeout,
    ))
