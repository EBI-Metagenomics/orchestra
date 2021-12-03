"""Base messenger class."""

from abc import ABC, abstractclassmethod
from typing import Any, Callable, Dict, Optional

from blackcap.schemas.message import Message


class BaseMessenger(ABC):
    """Base messenger class."""

    CONFIG_KEY = "MESSENGER"
    CONFIG_KEY_DEF_VAL = "GCP"

    # Change this value in custom auther implementations.
    CONFIG_KEY_VAL = "GCP"

    @abstractclassmethod
    def publish(self: "BaseMessenger", msg: Dict, topic_id: str) -> str:
        """Publish a msg.

        Args:
            msg (Dict): Message to publish
            topic_id (str): Id of the topic
        """
        pass

    @abstractclassmethod
    def subscribe(
        self: "BaseMessenger",
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
        pass

    @abstractclassmethod
    def parse_messenger_msg(self: "BaseMessenger", messenger_msg: Any) -> Message:
        """Parse messenger msg to blackcap mesage schema.

        Args:
            messenger_msg (Any): Messenger specific message
        """
        pass
