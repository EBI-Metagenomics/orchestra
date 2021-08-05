"""Job BLoCs."""

from typing import List

from conductor import DBSession
from conductor.models.job import JobDB
from conductor.schemas.api.job.delete import JobDelete
from conductor.schemas.api.job.get import JobGetQueryParams, JobQueryType
from conductor.schemas.api.job.post import JobCreate
from conductor.schemas.api.job.put import JobUpdate

from logzero import logger

from sqlalchemy import select


def create_job(job_create_list: List[JobCreate]) -> List[JobDB]:
    """Create jobs in the DB from JobCreate request.

    Args:
        job_create_list (List[JobCreate]): JobCreate request

    Returns:
        List[JobDB]: Instance of Job
    """
    with DBSession() as sesssion:
        try:
            job_db_create_list: List[JobDB] = [
                JobDB(
                    protagonist_id=job_create.user.id, **job_create.job.dict()
                )  # noqa: E501
                for job_create in job_create_list  # noqa: E501
            ]
            JobDB.bulk_create(job_db_create_list, sesssion)
            return job_db_create_list
        except Exception as e:
            sesssion.rollback()
            # TODO: Raise errors
            logger.error(f"Unable to create jobs: {e}")


def get_jobs(query_params: JobGetQueryParams) -> List[JobDB]:
    """Query DB for jobs.

    Args:
        query_params (JobGetQueryParams): Query params from request

    Returns:
        List[JobDB]: List of jobs returned from DB
    """
    job_list: List[JobDB] = []

    if query_params.query_type == JobQueryType.GET_ALL_JOBS:
        stmt = select(JobDB)
        with DBSession() as session:
            try:
                job_list: List[JobDB] = (
                    session.execute(stmt).scalars().all()
                )  # noqa: E501
                return job_list
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to fetch jobs due to {e}")
    if query_params.query_type == JobQueryType.GET_JOBS_BY_ID:
        stmt = select(JobDB).where(JobDB.id == query_params.job_id)
        with DBSession() as session:
            try:
                job_list: List[JobDB] = (
                    session.execute(stmt).scalars().all()
                )  # noqa: E501
                return job_list
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to fetch jobs due to {e}")
    if query_params.query_type == JobQueryType.GET_JOBS_BY_CLUSTER_ID:
        stmt = select(JobDB).where(JobDB.id == query_params.cluster_id)
        with DBSession() as session:
            try:
                job_list: List[JobDB] = (
                    session.execute(stmt).scalars().all()
                )  # noqa: E501
                return job_list
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to fetch jobs due to {e}")
    if query_params.query_type == JobQueryType.GET_JOBS_BY_PROTAGONIST_ID:
        stmt = select(JobDB).where(JobDB.id == query_params.protagonist_id)
        with DBSession() as session:
            try:
                job_list: List[JobDB] = (
                    session.execute(stmt).scalars().all()
                )  # noqa: E501
                return job_list
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to fetch jobs due to {e}")
    if query_params.query_type == JobQueryType.GET_JOBS_BY_STATUS:
        stmt = select(JobDB).where(JobDB.id == query_params.job_status)
        with DBSession() as session:
            try:
                job_list: List[JobDB] = (
                    session.execute(stmt).scalars().all()
                )  # noqa: E501
                return job_list
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to fetch jobs due to {e}")


def update_job(job_update: JobUpdate) -> JobDB:
    """Update job in the DB from JobUpdate request.

    Args:
        job_update (JobUpdate): JobUpdate request

    Returns:
        JobDB: Instance of Updated Job
    """
    stmt = select(JobDB).where(JobDB.id == job_update.id)
    with DBSession() as session:
        try:
            job_list: List[JobDB] = session.execute(stmt).scalars().all()  # noqa: E501
            if len(job_list) == 1:
                job_update_dict = job_update.dict()
                job_update_dict.pop("id")
                updated_job = job_list[0].update(
                    session, **job_update.dict()
                )  # noqa: E501
                return updated_job
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to update job: {job_update.dict()} due to {e}"
            )  # noqa: E501
            # TODO: Raise error


def delete_job(job_delete: JobDelete) -> JobDB:
    """Delete job in the DB from JobDelete request.

    Args:
        job_delete (JobDelete): JobDelete request

    Returns:
        JobDB: Instance of Deleted Job
    """
    stmt = select(JobDB).where(JobDB.id == job_delete.job_id)
    with DBSession() as session:
        try:
            job_list: List[JobDB] = session.execute(stmt).scalars().all()  # noqa: E501
            if len(job_list) == 1:
                deleted_job = job_list[0].delete(session)
                return deleted_job
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to delete job: {job_delete.dict()} due to {e}"
            )  # noqa: E501
            # TODO: Raise error
