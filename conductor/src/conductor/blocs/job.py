"""Job BLoCs."""

from datetime import datetime
from typing import List

from conductor import global_config
from conductor.extentions import messenger
from conductor.models.job import JobDB
from conductor.schemas.api.job.delete import JobDelete
from conductor.schemas.api.job.get import JobGetQueryParams
from conductor.schemas.api.job.post import JobCreate
from conductor.schemas.api.job.put import JobUpdate
from conductor.schemas.job import Job
from conductor.schemas.message import Message, MessageType

from logzero import logger


def create_job(job_create: JobCreate) -> JobDB:
    """Create job in the DB from JobCreate request.

    Args:
        job_create (JobCreate): JobCreate request

    Returns:
        JobDB: Instance of Job
    """
    try:
        job = JobDB(**job_create.job.dict())

        # try to publish msg before commiting
        message = Message(
            msg_type=MessageType.TO_DEMON_SCHEDULE_MSG,
            data=job_create.job.dict(),
            timestamp=str(datetime.now()),
        )
        messenger.publish(message, global_config.GCP_PUBSUB_TOPIC)

        # Commit to db and return job
        job.save()
        return job
    except Exception as e:
        logger.error(f"Unable to schedule msg: {e}")


def get_jobs(query_params: JobGetQueryParams) -> List[Job]:
    """Query DB for jobs.

    Args:
        query_params (JobGetQueryParams): Query params from request

    Returns:
        List[Job]: List of jobs returned from DB
    """
    pass


def update_job(job_update: JobUpdate) -> Job:
    """Update job in the DB from JobUpdate request.

    Args:
        job_update (JobUpdate): JobUpdate request

    Returns:
        JobDB: Instance of Updated Job
    """
    pass


def delete_job(job_delete: JobDelete) -> Job:
    """Delete job in the DB from JobDelete request.

    Args:
        job_delete (JobDelete): JobDelete request

    Returns:
        JobDB: Instance of Deleted Job
    """
    pass
