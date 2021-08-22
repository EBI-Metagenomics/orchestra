"""Publish tasks."""

from datetime import datetime
from typing import List

from demon import DBSession, celery_app, global_config
from demon.extentions import cluster
from demon.models.job import JobDB
from demon.models.schedule import ScheduleDB
from demon.schemas.job import Job
from demon.schemas.message import Message, MessageType
from demon.schemas.schedule import Schedule
from demon.tasks.pub_messenger import publish_messenger

from logzero import logger

from sqlalchemy import select


@celery_app.task
def publish_slurm_job_from_db() -> None:
    """Check for pending tasks in db and publish to slurm."""
    pending_schedules = []
    stmt = select(ScheduleDB).where(ScheduleDB.status == "PENDING")
    with DBSession() as session:
        pending_schedules: List[ScheduleDB] = (
            session.execute(stmt).scalars().all()
        )  # noqa: E501
        logger.info(f"Pending schedules: {len(pending_schedules)}")
        if len(pending_schedules) != 0:
            # fetch job
            stmt = select(JobDB).where(JobDB.id == pending_schedules[0].job_id)
            fetched_jobs = session.execute(stmt).scalars().all()
            if len(fetched_jobs) != 0:
                cluster.submit_job(
                    Schedule(
                        schedule_id=pending_schedules[0].id,
                        job_id=pending_schedules[0].job_id,
                        job=Job(
                            job_id=pending_schedules[0].job_id,
                            **fetched_jobs[0].to_dict(),
                        ),
                    )
                )
                pending_schedules[0].update(session, status="SUBMITTED")

                # Notify conductor that job is submitted
                publish_messenger(
                    Message(
                        msg_type=MessageType.TO_CONDUCTOR_JOB_STATUS_UPDATE,
                        data=Schedule(
                            schedule_id=pending_schedules[0].id,
                            **pending_schedules[0].to_dict(),
                        ),
                        timestamp=str(datetime.now()),
                    ).dict(),
                    topic_id=global_config.GCP_PUBSUB_TOPIC,
                )
            else:
                logger.error(
                    f"""
                    Unable to find job from schedule!!!
                    Schedule ID: {pending_schedules[0].id},
                    Job ID: {pending_schedules[0].job_id}
                    """
                )
