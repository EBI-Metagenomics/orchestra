"""Scheduler registry."""

from typing import Optional

from blackcap.scheduler.base import BaseScheduler


class SchedulerRegistry:
    """Scheduler registry."""

    schedulers = {}

    def add_scheduler(self: "SchedulerRegistry", scheduler: BaseScheduler) -> None:
        """Add custom schedulers to registry.

        Args:
            scheduler (BaseScheduler): Custom scheduler implementation
        """
        self.schedulers[scheduler.CONFIG_KEY_VAL] = scheduler

    def get_scheduler(
        self: "SchedulerRegistry", scheduler: str
    ) -> Optional[BaseScheduler]:  # noqa: E501
        """Get scheduler.

        Args:
            scheduler (str): Scheduler name

        Returns:
            Optional[BaseScheduler]: Returns the scheduler if found else None
        """
        return self.schedulers.get(scheduler)
