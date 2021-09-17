"""Blackcap DB commands."""

import click

from blackcap.db import db_engine
from blackcap.models.meta.mixins import DBModel


@click.command()
def init() -> None:
    """Init database."""
    click.secho("Creating database!", fg="green")
    DBModel.metadata.create_all(db_engine)


@click.command()
def destroy() -> None:
    """Destroy database."""
    click.secho("Destroying database!", fg="red")
    DBModel.metadata.drop_all(db_engine)


@click.command()
def reset() -> None:
    """Reset database."""
    DBModel.metadata.drop_all(db_engine)
    DBModel.metadata.create_all(db_engine)


@click.group()
def db() -> None:
    """Database commands."""
    pass


db.add_command(init)
db.add_command(destroy)
db.add_command(reset)
