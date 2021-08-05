"""Base Scheduler class."""

from abc import ABC, abstractclassmethod

from conductor.models.schedule import ScheduleDB
from conductor.schemas.api.schedule.post import ScheduleCreate


class BaseScheduler(ABC):
    """Base Scheduler class."""

    @abstractclassmethod
    def schedule(
        self: "BaseScheduler", schedule_create: ScheduleCreate
    ) -> ScheduleDB:  # noqa: E501
        """Create schedule from schedule request.

        Args:
            schedule_create (ScheduleCreate): Schedule create request

        Returns:
            ScheduleDB: Instance of ScheduleDB
        """
        return ScheduleDB()
