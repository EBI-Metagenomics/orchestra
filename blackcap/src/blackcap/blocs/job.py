"""Job BLoCs."""

from typing import List

from blackcap.db import DBSession
from blackcap.models.job import JobDB
from blackcap.schemas.api.job.delete import JobDelete
from blackcap.schemas.api.job.get import JobGetQueryParams, JobQueryType
from blackcap.schemas.api.job.post import JobCreate
from blackcap.schemas.api.job.put import JobUpdate
from blackcap.schemas.job import Job

from logzero import logger

from sqlalchemy import select


def create_job(job_create_list: List[JobCreate]) -> List[Job]:
    """Create jobs in the DB from JobCreate request.

    Args:
        job_create_list (List[JobCreate]): JobCreate request

    Raises:
        Exception: error

    Returns:
        List[Job]: List of created clusters
    """
    with DBSession() as session:
        try:
            job_db_create_list: List[JobDB] = [
                JobDB(
                    protagonist_id=job_create.user.user_id,
                    **job_create.job.dict(exclude={"job_id"}),  # noqa: E501
                )
                for job_create in job_create_list
            ]
            JobDB.bulk_create(job_db_create_list, session)
            return [
                Job(job_id=obj.id, **obj.to_dict())
                for obj in job_db_create_list  # noqa: E501
            ]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to create jobs: {e}")
            raise e


def get_jobs(query_params: JobGetQueryParams) -> List[Job]:
    """Query DB for jobs.

    Args:
        query_params (JobGetQueryParams): Query params from request

    Raises:
        Exception: error

    Returns:
        List[Job]: List of jobs returned from DB
    """
    job_list: List[JobDB] = []

    stmt = ""

    if query_params.query_type == JobQueryType.GET_ALL_JOBS:
        stmt = select(JobDB)
    if query_params.query_type == JobQueryType.GET_JOBS_BY_ID:
        stmt = select(JobDB).where(JobDB.id == query_params.job_id)
    if query_params.query_type == JobQueryType.GET_JOBS_BY_CLUSTER_ID:
        stmt = select(JobDB).where(JobDB.id == query_params.cluster_id)
    if query_params.query_type == JobQueryType.GET_JOBS_BY_PROTAGONIST_ID:
        stmt = select(JobDB).where(JobDB.id == query_params.protagonist_id)
    if query_params.query_type == JobQueryType.GET_JOBS_BY_STATUS:
        stmt = select(JobDB).where(JobDB.id == query_params.job_status)

    with DBSession() as session:
        try:
            job_list: List[JobDB] = session.execute(stmt).scalars().all()  # noqa: E501
            return [Job(job_id=obj.id, **obj.to_dict()) for obj in job_list]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch jobs due to {e}")
            raise e

    return job_list


def update_job(job_update: JobUpdate) -> Job:
    """Update job in the DB from JobUpdate request.

    Args:
        job_update (JobUpdate): JobUpdate request

    Raises:
        Exception: error

    Returns:
        Job: Instance of Updated Job
    """
    stmt = select(JobDB).where(JobDB.id == job_update.job_id)
    with DBSession() as session:
        try:
            job_list: List[JobDB] = session.execute(stmt).scalars().all()  # noqa: E501
            if len(job_list) == 1:
                job_update_dict = job_update.dict(exclude_defaults=True)
                job_update_dict.pop("job_id")
                updated_job = job_list[0].update(
                    session, **job_update_dict
                )  # noqa: E501
                return Job(job_id=updated_job.id, **updated_job.to_dict())
            if len(job_list) == 0:
                # TODO: Raise not found
                pass
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to update job: {job_update.dict()} due to {e}"
            )  # noqa: E501
            raise e


def delete_job(job_delete: JobDelete) -> Job:
    """Delete job in the DB from JobDelete request.

    Args:
        job_delete (JobDelete): JobDelete request

    Raises:
        Exception: error

    Returns:
        Job: Instance of Deleted Job
    """
    stmt = select(JobDB).where(JobDB.id == job_delete.job_id)
    with DBSession() as session:
        try:
            job_list: List[JobDB] = session.execute(stmt).scalars().all()  # noqa: E501
            if len(job_list) == 1:
                deleted_job = job_list[0].delete(session)
                return Job(job_id=deleted_job.id, **deleted_job.to_dict())
            if len(job_list) == 0:
                # TODO: Raise not found
                pass
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to delete job: {job_delete.dict()} due to {e}"
            )  # noqa: E501
            raise e
