"""Command-line interface."""

# flake8: noqa

import os

import click

from blackcap.cli.create import create
from blackcap.cli.db import db
from blackcap.cli.get import get
from blackcap.cli.publish import pub
from blackcap.cli.schedule import sched
from blackcap.cli.subscribe import sub
from blackcap.configs import config_registry
from blackcap.auther import auther_registry
from blackcap.schemas.api.auth.post import AuthUserCreds


from .. import __version__

config = config_registry.get_config()


@click.command()
@click.option("--email", required=True, help="email of user")
@click.option("--password", required=True, help="password of user")
def login(email, password) -> None:
    auth_creds = AuthUserCreds(email=email, password=password)
    auther = auther_registry.get_auther(config.AUTHER)
    login_tuple = auther.login_user(auth_creds)
    if login_tuple is None:
        click.secho("Login failed!", fg="red")
    else:
        click.secho(f"Your token: {login_tuple[1]}")
        click.secho(f"Add it to your env\n\n export USER_ACCESS_TOKEN={login_tuple[1]}")


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Conductor console."""
    pass


main.add_command(create)
main.add_command(get)
main.add_command(db)
main.add_command(pub)
main.add_command(sched)
main.add_command(login)
main.add_command(sub)
