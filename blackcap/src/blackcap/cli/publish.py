"""publish commands."""
# flake8: noqa: DAR101

from datetime import datetime
import random
from pathlib import Path

import click

from blackcap.configs import config_registry
from blackcap.schemas.message import Message, MessageType
from blackcap.messenger import messenger_registry

from logzero import logger

config = config_registry.get_config()
messenger = messenger_registry.get_messenger(config.MESSENGER)


@click.command()
@click.option(
    "--topic", default="test-topic", help="Id of the topic to publish msgs on"
)
def chatter(topic: str) -> None:
    """Publish a random msg."""
    logger.info("Trying to publish a random msg...")
    try:
        msg = f"Your lucky number is: {random.randint(1, 10)}"
        msg = Message(
            msg_type=MessageType.TO_DEMON_SCHEDULE_MSG,
            data={"msg": msg},
            timestamp=str(datetime.now()),
        )
        messenger.publish(msg.dict(), topic)
        logger.info(f"\nSuccess!\n\nMsg: {msg}")
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
        msg = Message(
            msg_type=MessageType.TO_DEMON_SCHEDULE_MSG,
            data={"msg": data},
            timestamp=str(datetime.now()),
        )
        messenger.publish(msg.dict(), topic)
        logger.info(f"\nSuccess!\n\nMsg: {data}")
    except Exception as e:
        logger.error(f"failed to publish msg: {e}")


@click.group()
def pub() -> None:
    """GCP pub/sub channel publish commands."""
    pass


pub.add_command(chatter)
pub.add_command(custom)
