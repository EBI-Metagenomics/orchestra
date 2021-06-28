"""Command-line interface."""

import click

from demon.cli.db import db
from demon.cli.subscribe import sub

from .. import __version__


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Demon console."""
    pass


main.add_command(sub)
main.add_command(db)
