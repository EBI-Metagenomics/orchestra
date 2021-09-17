"""Base Scheduler class."""

from abc import ABC, abstractclassmethod

from blackcap.schemas.api.schedule.post import ScheduleCreate
from blackcap.schemas.schedule import Schedule


class BaseScheduler(ABC):
    """Base Scheduler class."""

    CONFIG_KEY = "SCHEDULER"
    CONFIG_KEY_DEF_VAL = "RANDOM"

    # Change this value in custom auther implementations.
    CONFIG_KEY_VAL = "RANDOM"

    @abstractclassmethod
    def schedule(
        self: "BaseScheduler", schedule_create: ScheduleCreate
    ) -> Schedule:  # noqa: E501
        """Create schedule from schedule request.

        Args:
            schedule_create (ScheduleCreate): Schedule create request

        Returns:
            Schedule: Instance of Schedule
        """
        pass
