import click


@click.command()
@click.pass_obj
def get_credentials(credentials):
    click.echo("{} {}".format(
        credentials.username,
        credentials.password,
    ))
