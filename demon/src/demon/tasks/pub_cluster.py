"""Publish tasks."""

from typing import List

from demon import DBSession, celery_app
from demon.extentions import cluster
from demon.models.job import JobDB
from demon.schemas.job import Job

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
            cluster.submit_job(
                Job(job_id=pending_jobs[0].id, **pending_jobs[0].to_dict())
            )
            pending_jobs[0].update(session, status="SUBMTTED")
            # TODO: Notify conductor that job is submitted
