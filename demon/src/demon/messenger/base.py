"""Base messenger class."""

from abc import ABC, abstractclassmethod, abstractmethod
from typing import Any, Callable, Optional

from demon.schemas.message import Message


class BaseMessenger(ABC):
    """Base messenger class."""

    @abstractclassmethod
    def publish(
        self: "BaseMessenger", msg: Message, topic_id: str
    ) -> str:  # noqa: E501
        """Publish a msg.

        Args:
            msg (Message): Message to publish
            topic_id (str): Id of the topic
        """
        pass

    @abstractclassmethod
    def subscribe(
        self: "BaseMessenger",
        callback: Callable,
        sub_id: str,
        timeout: Optional[float] = None,
    ) -> None:  # noqa: E501
        """Subscribe to a topic.

        Args:
            callback (Callable): Callback to invoke when a msg is received
            sub_id (str): Id of the topic.
            timeout (Union[float, None]): Time to wait for msgs. Defaults to None. # noqa: E501
        """
        pass

    @abstractmethod
    def process_schedule_msg(self: "BaseMessenger", msg: Any) -> None:
        """Save jobs to DB from Pub/Sub msgs.

        Args:
            msg (Any): Pub/Sub Msg
        """
        pass

    @abstractmethod
    def echo_msg(self: "BaseMessenger", msg: Message) -> None:
        """Echo msgs to stdout.

        Args:
            msg (Message): Message to echo
        """
        pass
