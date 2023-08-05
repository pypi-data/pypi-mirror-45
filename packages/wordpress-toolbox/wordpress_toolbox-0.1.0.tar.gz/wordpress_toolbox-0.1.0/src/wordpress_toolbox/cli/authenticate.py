import click


from ..utils import set_credentials


@click.command()
@click.argument("username")
@click.argument("password")
@click.pass_obj
def authenticate(options, username, password):
    set_credentials(options.url, username, password)
