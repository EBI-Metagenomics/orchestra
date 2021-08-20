"""Command-line interface."""

# flake8: noqa

import os

import click

from conductor.cli.create import create
from conductor.cli.db import db
from conductor.cli.get import get
from conductor.cli.publish import pub
from conductor.cli.schedule import sched
from conductor.extentions import auther
from conductor.schemas.api.auth.post import AuthUserCreds


from .. import __version__


@click.command()
@click.option("--email", required=True, help="email of user")
@click.option("--password", required=True, help="password of user")
def login(email, password) -> None:
    auth_creds = AuthUserCreds(email=email, password=password)
    login_tuple = auther.login_user(auth_creds)
    if login_tuple is None:
        click.secho("Login failed!", fg="red")
    else:
        click.secho(f"Your token: {login_tuple[1]}")
        click.secho(f"Adding it to your env...")


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
