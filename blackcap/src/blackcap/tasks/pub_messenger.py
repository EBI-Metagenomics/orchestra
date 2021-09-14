"""Task to publish msgs to GCP Pub/Sub topic."""

from blackcap import celery_app
from blackcap.extensions import messenger
from blackcap.schemas.message import Message

from logzero import logger


@celery_app.task
def publish_messenger(msg: Message, topic_id: str) -> None:
    """Publish msgs to GCP Pub/Sub topic.

    Args:
        msg (Message): msg to publish
        topic_id (str): Id of the topic

    Raises:
        Exception: error
    """
    try:
        messenger.publish(msg=msg, topic_id=topic_id)
    except Exception as e:
        logger.error(e)
        raise e
