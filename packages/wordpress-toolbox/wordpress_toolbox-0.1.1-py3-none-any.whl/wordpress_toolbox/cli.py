import click

from .utils import make_url, make_request
from .settings import DEFAULT_TIMEOUT, POSTS_SUFFIX


@click.group()
def main():
    pass


@main.command()
@click.argument("url")
@click.argument("timeout", default=DEFAULT_TIMEOUT)
def get_posts(url, timeout):
    url = make_url(url, POSTS_SUFFIX)
    res = make_request("get", url, timeout)
    click.echo(res)


@main.command()
@click.argument("url")
@click.argument("id")
@click.option("--timeout", default=DEFAULT_TIMEOUT)
def get_post(url, id, timeout):
    url = make_url(url, POSTS_SUFFIX, id)
    res = make_request("get", url, timeout)
    click.echo(res)


@main.command()
@click.argument("url")
@click.option("--timeout", default=DEFAULT_TIMEOUT)
@click.option("--date")
@click.option("--date_gmt")
@click.option("--slug")
@click.option("--status")
@click.option("--password")
@click.option("--title")
@click.option("--content")
@click.option("--author")
@click.option("--excerpt")
@click.option("--featured_media")
@click.option("--comment_status")
@click.option("--ping_status")
@click.option("--format")
@click.option("--meta")
@click.option("--sticky")
@click.option("--template")
@click.option("--categories")
@click.option("--tags")
def create_post(url, timeout, date, date_gmt, slug, status, password, title,
                content, author, excerpt, featured_media, comment_status,
                ping_status, format, meta, sticky, template, categories,
                tags):
    url = make_url(url, POSTS_SUFFIX)
    data = {
        "url": url,
        "date": date,
        "date_gmt": date_gmt,
        "slug": slug,
        "status": status,
        "password": password,
        "title": title,
        "content": content,
        "author": author,
        "excerpt": excerpt,
        "featured_media": featured_media,
        "comment_status": comment_status,
        "ping_status": ping_status,
        "format": format,
        "meta": meta,
        "sticky": sticky,
        "template": template,
        "categories": categories,
        "tags": tags,
    }
    res = make_request("post", url, timeout, data)
    click.echo(res)


if __name__ == "__main__":
    main()
