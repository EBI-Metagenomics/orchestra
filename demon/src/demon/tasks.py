"""Celery tasks."""

from typing import Any, List

from demon.extentions import DBSession, celery_app
from demon.schemas.jobs.base import BaseJobDB, JobStatus
from demon.utils.slurm_callbacks import submit_slurm_job

from sqlalchemy import select


@celery_app.task
def publish_slurm_job_from_db() -> None:
    """Check for pending tasks in db and publish to slurm."""
    pending_jobs = []
    stmt = select(BaseJobDB).where(BaseJobDB.status == "PENDING")
    with DBSession() as session:
        pending_jobs: List[BaseJobDB] = session.execute(stmt).scalars().all()
        print(f"Pending jobs: {len(pending_jobs)}")
        if len(pending_jobs) != 0:
            submit_slurm_job(pending_jobs[0])
            pending_jobs[0].update(session, status=JobStatus.RUNNING.value)


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
