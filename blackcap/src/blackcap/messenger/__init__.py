"""Messenger that delivers and reads msgs from a pub/sub queue."""

from enum import Enum, unique
from functools import lru_cache

from blackcap import global_config
from blackcap.messenger.base import BaseMessenger
from blackcap.messenger.gcp_messenger import GCPMessenger


@unique
class MessengerEnum(Enum):
    """Messenger enum."""

    GCP = GCPMessenger


@lru_cache()
def get_messenger() -> BaseMessenger:
    """Cache and return Messenger object.

    Returns:
        BaseMessenger: An instance of a class that inherits BaseMessenger
    """
    return MessengerEnum[global_config.MESSENGER].value(global_config)
