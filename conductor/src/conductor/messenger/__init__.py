"""Messenger that delivers and reads msgs from a pub/sub queue."""

from enum import Enum, unique

from conductor.messenger.gcp_messenger import GCPMessenger


@unique
class MessengerEnum(Enum):
    """Messenger enum."""

    GCP = GCPMessenger
