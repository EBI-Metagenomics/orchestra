"""Observer to fetch metrcis from a central monitoring system."""

from enum import Enum, unique
from functools import lru_cache

from conductor import global_config
from conductor.observer.base import BaseObserver
from conductor.observer.elastic_observer import ElasticObserver


@unique
class ObserverEnum(Enum):
    """Observer enum."""

    ELASTIC = ElasticObserver


@lru_cache()
def get_observer() -> BaseObserver:
    """Cache and return Observer object.

    Returns:
        BaseObserver : An instance of a class that inherits BaseObserver
    """
    return ObserverEnum[global_config.OBSERVER].value()
