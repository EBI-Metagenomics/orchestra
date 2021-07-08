"""Job BLoCs."""

from typing import List

from conductor.models.job import JobDB
from conductor.schemas.api.job.post import JobCreate
from conductor.schemas.api.job.get import JobGetQueryParams
from conductor.schemas.job import Job


def create_job(job_create: JobCreate) -> JobDB:
    """Create job in the DB from JobCreate request.

    Args:
        job_create (JobCreate): JobCreate request

    Returns:
        JobDB: Instance of SQLAlchemy model JobDB
    """
    pass


def get_jobs(query_params: JobGetQueryParams) -> List[Job]:
    """Query DB for jobs.

    Args:
        query_params (JobGetQueryParams): Query params from request

    Returns:
        List[Job]: List of jobs returned from DB
    """
    pass
