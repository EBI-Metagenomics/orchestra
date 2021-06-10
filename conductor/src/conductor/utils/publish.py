"""Utility function to publish messages to GCP Pub/Sub topics."""

from typing import Union

from google.cloud import pubsub_v1


def publish_msg(msg: str, topic_id: str, timeout: Union[float, None]) -> str:
    """Publish msgs on GCP Pub/Sub topics.

    Args:
        msg (str): msg to publish
        topic_id(str): topic id to publish on
        timeout(Union[float, None]): time to wait in seconds before giving up

    Returns:
        str: The message ID
    """
    project_id = ""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Msg must be a bytestring
    msg = msg.encode("utf-8")

    # Wait for the returned future
    future = publisher.publish(topic_path, msg)
    return future.result()
