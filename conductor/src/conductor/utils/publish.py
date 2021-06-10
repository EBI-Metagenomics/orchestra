"""Utility function to publish messages to GCP Pub/Sub topics."""

from typing import Union

from conductor.configs import get_config
from conductor.configs.base import BaseConfig

from google.cloud import pubsub_v1

# Initialize default config at module level
default_config = get_config()


def publish_msg(
    msg: str,
    topic_id: str,
    timeout: Union[float, None] = None,
    config: BaseConfig = default_config,
) -> str:
    """Publish msgs on GCP Pub/Sub topics.

    Args:
        msg (str): msg to publish
        topic_id(str): topic id to publish on
        timeout(Union[float, None]): time to wait in seconds before giving up
        config(BaseConfig): Project config to use

    Returns:
        str: The message ID
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(config.GCP_PROJECT_ID, topic_id)

    # Msg must be a bytestring
    msg = msg.encode("utf-8")

    # Wait for the returned future
    future = publisher.publish(topic_path, msg)
    return future.result()
