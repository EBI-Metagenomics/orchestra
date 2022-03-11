"""Base Scheduler class."""

from abc import ABC, abstractclassmethod

from blackcap.schemas.api.schedule.post import ScheduleCreate


class BaseScheduler(ABC):
    """Base Scheduler class."""

    CONFIG_KEY = "SCHEDULER"
    CONFIG_KEY_DEF_VAL = "RANDOM"

    # Change this value in custom auther implementations.
    CONFIG_KEY_VAL = "RANDOM"

    @abstractclassmethod
    def schedule(
        self: "BaseScheduler", schedule_create: ScheduleCreate
    ) -> ScheduleCreate:
        """Create schedule from schedule request.

        Args:
            schedule_create (ScheduleCreate): Schedule create request

        Returns:
            ScheduleCreate: Instance of Schedule
        """
        return ScheduleCreate()
