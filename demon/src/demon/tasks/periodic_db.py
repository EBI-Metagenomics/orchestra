"""Celery tasks."""

from typing import Any

from demon import celery_app
from demon.tasks.pub_cluster import publish_slurm_job_from_db


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Any, **kwargs: Any) -> None:
    """Set up periodic tasks.

    Args:
        sender (Any): Sender
        **kwargs (Any): Kwargs
    """
    # Calls publish_slurm_job_from_db() every 10 seconds.
    sender.add_periodic_task(
        10.0, publish_slurm_job_from_db.s(), name="Submit jobs every 10s"
    )
