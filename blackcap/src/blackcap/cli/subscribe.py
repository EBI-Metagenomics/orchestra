"""subscribe commands."""
# flake8: noqa: DAR101

from backoff import expo, on_exception
import click
from logzero import logger

from blackcap.configs import config_registry
from blackcap.messenger import messenger_registry
from blackcap.cluster import cluster_registry


config = config_registry.get_config()
messenger = messenger_registry.get_messenger(config.MESSENGER)
cluster = cluster_registry.get_cluster(config.CLUSTER)


@click.command()
@click.option("--sub_id", default=config.MESSENGER_SUB_ID, help="Subscription Id")
def echo(sub_id: str) -> None:
    """subscribe and echo msgs"""
    logger.info("Trying to subscribe and read messages...")
    try:
        messenger.subscribe(callback=messenger.echo_msg, sub_id=sub_id)
    except Exception as e:
        logger.error(f"failed to subscribe: {e}")


@click.command()
@click.option("--sub_id", default=config.MESSENGER_SUB_ID, help="Subscription Id")
@on_exception(expo, Exception)
def schedule(sub_id: str) -> None:
    """subscribe and save msgs to DB"""
    logger.info("Trying to subscribe and read messages...")
    try:
        messenger.subscribe(callback=cluster.process_schedule_msg, sub_id=sub_id)
    except Exception as e:
        logger.error(f"failed to subscribe: {e}")


@click.group()
def sub() -> None:
    """GCP pub/sub channel subscribe commands."""
    pass


sub.add_command(echo)
sub.add_command(schedule)
