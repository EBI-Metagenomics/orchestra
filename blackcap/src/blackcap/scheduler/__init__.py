"""Scheduler to schedule jobs using metrcis from clusters."""

from enum import Enum, unique
from functools import lru_cache

from blackcap import global_config
from blackcap.scheduler.base import BaseScheduler
from blackcap.scheduler.random_scheduler import RandomScheduler


@unique
class SchedulerEnum(Enum):
    """Scheduler enum."""

    RANDOM = RandomScheduler


@lru_cache()
def get_scheduler() -> BaseScheduler:
    """Cache and return Scheduler object.

    Returns:
        BaseScheduler : An instance of a class that inherits BaseScheduler
    """
    return SchedulerEnum[global_config.SCHEDULER].value()
