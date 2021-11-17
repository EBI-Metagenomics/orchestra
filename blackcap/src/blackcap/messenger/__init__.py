"""Messenger that delivers and reads msgs from a pub/sub queue."""

from blackcap.configs import config_registry
from blackcap.messenger.gcp_messenger import GCPMessenger
from blackcap.messenger.nats_messenger import NATSMessenger
from blackcap.messenger.registry import MessengerRegistry

config = config_registry.get_config()

messenger_registry = MessengerRegistry()
messenger_registry.add_messenger(GCPMessenger(config))
messenger_registry.add_messenger(NATSMessenger(config))
