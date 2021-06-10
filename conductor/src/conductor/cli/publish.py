"""publish commands."""
# flake8: noqa: DAR101

import random
from pathlib import Path

import click

from conductor.utils.publish import publish_msg

from logzero import logger


@click.command()
@click.option(
    "--topic", default="test-topic", help="Id of the topic to publish msgs on"
)
def chatter(topic: str) -> None:
    """Publish a random msg."""
    logger.info("Trying to publish a random msg...")
    try:
        msg = f"Your lucky number is: {random.randint(1, 10)}"
        msg_id = publish_msg(msg, topic)
        logger.info(f"\nSuccess!\nMsg ID: {msg_id}\nMsg: {msg}")
    except Exception as e:
        logger.error(f"failed to publish msg: {e}")


@click.command()
@click.option(
    "--topic", default="test-topic", help="Id of the topic to publish msgs on"
)
@click.option("--data", help="custom string to publish", required=True)
def custom(topic: str, data: str) -> None:
    """Publish user provided string."""
    logger.info("Trying to publish a custom string...")
    try:
        msg_id = publish_msg(data, topic)
        logger.info(f"\nSuccess!\nMsg ID: {msg_id}\nMsg: {data}")
    except Exception as e:
        logger.error(f"failed to publish msg: {e}")


@click.command()
@click.option(
    "--topic", default="test-topic", help="Id of the topic to publish msgs on"
)
@click.option("--file", help="file path of job's JSON file", required=True)
def job(topic: str, file: str) -> None:
    """Publish a job."""
    logger.info("Trying to publish a job...")
    try:
        job_file_path = Path(file)
        with open(job_file_path) as job_file:
            data = job_file.read()
            msg_id = publish_msg(data, topic)
            logger.info(f"\nSuccess!\nMsg ID: {msg_id}\nMsg: {data}")
    except Exception as e:
        logger.error(f"failed to publish msg: {e}")


@click.group()
def pub() -> None:
    """GCP pub/sub channel publish commands."""
    pass


pub.add_command(chatter)
pub.add_command(custom)
pub.add_command(job)
