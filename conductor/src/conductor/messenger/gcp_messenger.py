"""GCP implementation of messenger."""

import json
from typing import Callable, Dict, Optional

from conductor.configs.base import BaseConfig
from conductor.messenger.base import BaseMessenger

from google.auth import jwt
from google.cloud import pubsub_v1

from logzero import logger


class GCPMessenger(BaseMessenger):
    """GCP(Pub/Sub) implementation of Messenger."""

    def __init__(self: "GCPMessenger", config: BaseConfig) -> None:
        """Initialize Messenger with app config.

        Args:
            config (BaseConfig): Config to initialize messenger
        """
        self.pub_audience = (
            "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"  # noqa: E501
        )
        self.sub_audience = (
            "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"  # noqa: E501
        )
        self.service_account_info = json.load(
            open(config.GOOGLE_APPLICATION_CREDENTIALS)
        )  # noqa: E501
        self.pub_credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=self.pub_audience
        )

        self.sub_credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=self.sub_audience
        )

        self.publisher = pubsub_v1.PublisherClient(
            credentials=self.pub_credentials
        )  # noqa: E501

        self.subscriber = pubsub_v1.SubscriberClient(
            credentials=self.sub_credentials
        )  # noqa: E501
        self.project_id = config.GCP_PROJECT_ID

    def publish(self: "GCPMessenger", msg: Dict, topic_id: str) -> str:
        """Publish msg on the GCP Pub/Sub queue.

        Args:
            msg (Dict): Messsag to publish
            topic_id (str): Id of the topic

        Returns:
            str: Id of the published msg
        """
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Msg must be a bytestring

        msg = json.dumps(msg).encode("utf-8")

        # Wait for the returned future
        future = self.publisher.publish(topic_path, msg)
        return future.result()

    def subscribe(
        self: "GCPMessenger",
        callback: Callable,
        sub_id: str,
        timeout: Optional[float] = None,  # noqa: E501
    ) -> None:
        """Subscribe to a topic.

        Args:
            callback (Callable): Callback to invoke when a msg is received
            sub_id (str): Id of the topic.
            timeout (Union[float, None]): Time to wait for msgs. Defaults to None. # noqa: E501
        """
        subscription_path = self.subscriber.subscription_path(
            self.project_id, sub_id
        )  # noqa: E501

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback,
            await_callbacks_on_shutdown=True,  # noqa: E501
        )

        with self.subscriber:
            try:
                streaming_pull_future.result(timeout=timeout)
            except TimeoutError as e:
                logger.error(
                    f"GCPMessenger timeout error while pulling messages. Error: {e}"  # noqa: E501
                )  # noqa: E501
                streaming_pull_future.cancel()
