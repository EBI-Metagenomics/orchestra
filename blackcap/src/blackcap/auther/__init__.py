"""Auther to handle authentication and authorizations."""

from blackcap.auther.cookie_auther import CookieAuther
from blackcap.auther.registry import AutherRegistry


auther_registry = AutherRegistry()
# Add auther implementations to the registry
auther_registry.add_auther(CookieAuther())
