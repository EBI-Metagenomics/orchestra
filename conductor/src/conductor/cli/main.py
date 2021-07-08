"""Command-line interface."""

import click

from conductor.cli.db import db
from conductor.cli.publish import pub

from .. import __version__


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Conductor console."""
    pass


main.add_command(db)
main.add_command(pub)
