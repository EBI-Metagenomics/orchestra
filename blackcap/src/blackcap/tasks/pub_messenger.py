"""Task to publish msgs to GCP Pub/Sub topic."""

from blackcap.configs import config_registry
from blackcap.messenger import messenger_registry
from blackcap.schemas.message import Message
from blackcap.workers import celery_app

from logzero import logger

config = config_registry.get_config()
messenger = messenger_registry.get_messenger(config.MESSENGER)


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
