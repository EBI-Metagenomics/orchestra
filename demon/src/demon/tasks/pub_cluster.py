"""Publish tasks."""

from typing import List

from demon.extentions import DBSession, celery_app
from demon.models.job import JobDB
from demon.utils.slurm_callbacks import submit_slurm_job

from sqlalchemy import select


@celery_app.task
def publish_slurm_job_from_db() -> None:
    """Check for pending tasks in db and publish to slurm."""
    pending_jobs = []
    stmt = select(JobDB).where(JobDB.status == "PENDING")
    with DBSession() as session:
        pending_jobs: List[JobDB] = session.execute(stmt).scalars().all()
        print(f"Pending jobs: {len(pending_jobs)}")
        if len(pending_jobs) != 0:
            submit_slurm_job(pending_jobs[0])
            pending_jobs[0].update(session, status="SUBMTTED")
            # TODO: Notify conductor that job is submitted
