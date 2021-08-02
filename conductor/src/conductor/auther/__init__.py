"""Auther to handle authentication and authorizations."""

from enum import Enum, unique
from functools import lru_cache

from conductor import global_config
from conductor.auther.base import BaseAuther
from conductor.auther.cookie_auther import CookieAuther


@unique
class AutherEnum(Enum):
    """Auther enum."""

    COOKIE = CookieAuther


@lru_cache()
def get_auther() -> BaseAuther:
    """Cache and return Auther object.

    Returns:
        BaseAuther : An instance of a class that inherits BaseAuther
    """
    return AutherEnum[global_config.AUTHER].value()
