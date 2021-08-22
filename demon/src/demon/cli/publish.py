"""publish commands."""
# flake8: noqa: DAR101

from datetime import datetime

import click

from demon import global_config
from demon.schemas.message import Message, MessageType
from demon.schemas.schedule import Schedule
from demon.tasks.pub_messenger import publish_messenger

from logzero import logger


@click.command()
@click.option(
    "--topic", default="test-topic", help="Id of the topic to publish msgs on"
)
@click.option("--sched_id", help="schedule id", required=True)
@click.option("--job_id", help="job id", required=True)
@click.option("--status", help="status of the job", required=True)
def schedup(sched_id: str, job_id: str, status: str) -> None:
    """Publish schedule update."""
    logger.info("Trying to publish schedule update")
    try:
        publish_messenger(
            Message(
                msg_type=MessageType.TO_CONDUCTOR_JOB_STATUS_UPDATE,
                data=Schedule(schedule_id=sched_id, job_id=job_id, status=status),
                timestamp=str(datetime.now()),
            ).dict(),
            topic_id=global_config.GCP_PUBSUB_TOPIC,
        )
    except Exception as e:
        logger.error(f"failed to publish schedule update: {e}")


@click.group()
def pub() -> None:
    """GCP pub/sub channel publish commands."""
    pass


pub.add_command(schedup)
