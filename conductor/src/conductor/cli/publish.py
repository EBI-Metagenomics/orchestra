"""publish commands."""

import random

import click

from conductor.utils.publish import publish_msg


@click.command()
@click.option(
    "--topic", default="test-topic", help="Id of the topic to publish msgs on"
)
def random_msg(topic: str) -> None:
    """Publish a random msg.

    Args:
        topic (str): Id of the topic to publish msgs on
    """
    publish_msg(random.randint(), topic)  # noqa: S311


@click.group()
def publish() -> None:
    """GCP pub/sub channel publish commands."""
    pass


publish.add_command(random_msg)
