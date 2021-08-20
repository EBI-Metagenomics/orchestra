"""Base Scheduler class."""

from abc import ABC, abstractclassmethod

from conductor.schemas.api.schedule.post import ScheduleCreate
from conductor.schemas.schedule import Schedule


class BaseScheduler(ABC):
    """Base Scheduler class."""

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
