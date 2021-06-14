"""Task to publish msgs to GCP Pub/Sub topic."""

from conductor.extensions import celery_app
from conductor.utils.publish import publish_msg

from logzero import logger


@celery_app.task
def publish_gcp_msg(msg: str) -> None:
    """Publish msgs to GCP Pub/Sub topic.

    Args:
        msg (str): msg to publish
    """
    try:
        publish_msg(msg=msg)
    except Exception as e:
        logger.error(e)
