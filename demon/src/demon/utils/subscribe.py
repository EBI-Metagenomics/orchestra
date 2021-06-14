"""Utility function to subscribe messages from GCP Pub/Sub topics."""

import json
from concurrent.futures import TimeoutError
from typing import Callable, Union


from demon.configs import get_config
from demon.configs.base import BaseConfig

from google.auth import jwt
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message


# Initialize default config at module level
default_config = get_config()


def echo_msg(msg: Message) -> None:
    """Echo msgs to stout.

    Args:
        msg (Message): Message to echo
    """
    print(msg)
    msg.ack()


def subscribe_topic(
    sub_id: str,
    callback: Callable[[Message], None],
    timeout: Union[float, None] = None,
    config: BaseConfig = default_config,
) -> None:
    """Subscribe to GCP Pub/Sub topics.

    Args:
        sub_id (str): Subscription ID to use
        callback (Callable[Message]): Function to process received messages
        timeout (Union[float, None]): Time to wait for msgs. Defaults to None.
        config (BaseConfig): Project config to use. Defaults to default_config.
    """
    audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
    service_account_info = json.load(
        open(config.GOOGLE_APPLICATION_CREDENTIALS)
    )  # noqa: E501
    credentials = jwt.Credentials.from_service_account_info(
        service_account_info, audience=audience
    )
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    subscription_path = subscriber.subscription_path(
        config.GCP_PROJECT_ID, sub_id
    )  # noqa: E501

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, await_callbacks_on_shutdown=True
    )  # noqa: E501

    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
