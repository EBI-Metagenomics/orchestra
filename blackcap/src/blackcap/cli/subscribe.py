"""subscribe commands."""
# flake8: noqa: DAR101

import click

from blackcap import global_config
from blackcap.extensions import messenger

from logzero import logger


@click.command()
@click.option(
    "--sub_id", default=global_config.GCP_PUBSUB_SUB_ID, help="Subscription Id"
)
def echo(sub_id: str) -> None:
    """subscribe and echo msgs"""
    logger.info("Trying to subscribe and read messages...")
    try:
        messenger.subscribe(callback=messenger.echo_msg, sub_id=sub_id)
    except Exception as e:
        logger.error(f"failed to subscribe: {e}")


@click.command()
@click.option(
    "--sub_id", default=global_config.GCP_PUBSUB_SUB_ID, help="Subscription Id"
)
def schedule(sub_id: str) -> None:
    """subscribe and save msgs to DB"""
    logger.info("Trying to subscribe and read messages...")
    try:
        messenger.subscribe(callback=messenger.process_schedule_msg, sub_id=sub_id)
    except Exception as e:
        logger.error(f"failed to subscribe: {e}")


@click.group()
def sub() -> None:
    """GCP pub/sub channel subscribe commands."""
    pass


sub.add_command(echo)
sub.add_command(schedule)
