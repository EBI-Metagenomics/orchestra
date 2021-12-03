"""GCP implementation of messenger."""

import json
from typing import Callable, Dict, Optional

from blackcap.configs.base import BaseConfig
from blackcap.messenger.base import BaseMessenger
from blackcap.schemas.message import Message
from blackcap.utils.json_encoders import UUIDEncoder

from google.auth import jwt
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message as GCPMessage

from logzero import logger

from sqlalchemy import select


class GCPMessenger(BaseMessenger):
    """GCP(Pub/Sub) implementation of Messenger."""

    CONFIG_KEY_VAL = "GCP"

    def __init__(self: "GCPMessenger", config: BaseConfig) -> None:
        """Initialize Messenger with app config.

        Args:
            config (BaseConfig): Config to initialize messenger
        """
        self.pub_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
        self.sub_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"

        self.config = config

        self.project_id = config.GCP_PROJECT_ID

    @property
    def service_account_info(self: "GCPMessenger") -> Dict:
        """Service account info."""
        return json.load(open(self.config.GOOGLE_APPLICATION_CREDENTIALS))

    @property
    def publisher(self: "GCPMessenger") -> pubsub_v1.PublisherClient:
        """Publisher Client."""
        self.pub_credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=self.pub_audience
        )
        return pubsub_v1.PublisherClient(credentials=self.pub_credentials)

    @property
    def subscriber(self: "GCPMessenger") -> pubsub_v1.SubscriberClient:
        """Subscriber Client."""
        self.sub_credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=self.sub_audience
        )
        return pubsub_v1.SubscriberClient(credentials=self.sub_credentials)

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

        msg = json.dumps(msg, cls=UUIDEncoder).encode("utf-8")

        # Wait for the returned future
        future = self.publisher.publish(topic_path, msg)
        return future.result()

    def subscribe(
        self: "GCPMessenger",
        callback: Callable,
        sub_id: str,
        timeout: Optional[float] = None,
    ) -> None:
        """Subscribe to a topic.

        Args:
            callback (Callable): Callback to invoke when a msg is received
            sub_id (str): Id of the topic.
            timeout (Union[float, None]): Time to wait for msgs. Defaults to None. # noqa: E501
        """
        subscription_path = self.subscriber.subscription_path(self.project_id, sub_id)

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback,
            await_callbacks_on_shutdown=True,
        )

        with self.subscriber:
            try:
                streaming_pull_future.result(timeout=timeout)
            except TimeoutError as e:
                logger.error(
                    f"GCPMessenger timeout error while pulling messages. Error: {e}"
                )
                streaming_pull_future.cancel()

    def parse_messenger_msg(self: "GCPMessenger", messenger_msg: GCPMessage) -> Message:
        return Message.parse_raw(messenger_msg.data)

    def echo_msg(self: "GCPMessenger", msg: Message) -> None:
        """Echo msgs to stdout.

        Args:
            msg (Message): Message to echo
        """
        print(msg)
        msg.ack()
