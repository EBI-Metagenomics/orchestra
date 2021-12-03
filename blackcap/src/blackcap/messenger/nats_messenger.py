"""NATS implementation of messenger."""

from dataclasses import asdict
import json
from typing import Callable, Dict, Optional

from blackcap.configs.base import BaseConfig
from blackcap.messenger.base import BaseMessenger
from blackcap.schemas.message import Message
from blackcap.utils.json_encoders import UUIDEncoder

from logzero import logger

from pynats import NATSClient, NATSMessage


class NATSMessenger(BaseMessenger):
    """NATS implementation of Messenger."""

    CONFIG_KEY_VAL = "NATS"

    def __init__(self: "NATSMessenger", config: BaseConfig) -> None:
        """Initialize Messenger with app config.

        Args:
            config (BaseConfig): Config to initialize messenger
        """

        self.config = config

    @property
    def client(self: "NATSMessenger") -> NATSClient:
        """NATS client object."""
        client = NATSClient(url=self.config.NATS_ENDPOINT, name=self.config.FLASK_APP)
        client.connect()
        return client

    def publish(self: "NATSMessenger", msg: Dict, topic_id: str) -> str:
        """Publish msg on the GCP Pub/Sub queue.

        Args:
            msg (Dict): Messsag to publish
            topic_id (str): Id of the topic

        Returns:
            str: Id of the published msg
        """
        # Msg must be a bytestring
        msg = json.dumps(msg, cls=UUIDEncoder).encode("utf-8")
        self.client.publish(subject=topic_id, payload=msg)
        self.client.close()
        return "ok"

    def subscribe(
        self: "NATSMessenger",
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
        try:
            client = self.client
            sub = client.subscribe(subject=sub_id, callback=callback)
            logger.info(f"Subscription created: {sub}")
            client.wait(count=None)
            client.close()
        except Exception as e:
            logger.error(
                f"NATSMessenger subscribe error while pulling messages. Error: {e}"
            )
            client.close()

    def parse_messenger_msg(
        self: "NATSMessenger", messenger_msg: NATSMessage
    ) -> Message:
        return Message.parse_obj(asdict(messenger_msg))

    def echo_msg(self: "NATSMessenger", msg: NATSMessage) -> None:
        """Echo msgs to stdout.

        Args:
            msg (NATSMessage): Message to echo
        """
        print(asdict(msg))
