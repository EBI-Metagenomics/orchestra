"""Scheduler to schedule jobs using metrcis from clusters."""

from blackcap.scheduler.random_scheduler import RandomScheduler
from blackcap.scheduler.registry import SchedulerRegistry

scheduler_registry = SchedulerRegistry()
scheduler_registry.add_scheduler(RandomScheduler())
