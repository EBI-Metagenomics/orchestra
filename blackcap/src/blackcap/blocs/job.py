"""Job BLoCs."""

from typing import List

from logzero import logger
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from blackcap.db import DBSession
from blackcap.flow import Flow, FlowExecError, FuncProp, get_outer_function, Prop, Step
from blackcap.flow.step import dummy_backward
from blackcap.models.job import JobDB
from blackcap.schemas.api.job.delete import JobDelete
from blackcap.schemas.api.job.get import JobGetQueryParams, JobQueryType
from blackcap.schemas.api.job.post import JobCreate
from blackcap.schemas.api.job.put import JobUpdate
from blackcap.schemas.job import Job
from blackcap.schemas.user import User

###
# CRUD BLoCs
###


def create_job(job_create_list: List[JobCreate], user_creds: User) -> List[Job]:
    """Create jobs in the DB from JobCreate request.

    Args:
        job_create_list (List[JobCreate]): JobCreate request
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        List[Job]: List of created clusters
    """
    with DBSession() as session:
        try:
            job_db_create_list: List[JobDB] = [
                JobDB(
                    protagonist_id=user_creds.user_id,
                    **job_create.dict(),
                )
                for job_create in job_create_list
            ]
            JobDB.bulk_create(job_db_create_list, session)
            return [Job(job_id=obj.id, **obj.to_dict()) for obj in job_db_create_list]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to create jobs: {e}")
            raise e


def get_job(  # noqa: C901
    query_params: JobGetQueryParams, user_creds: User
) -> List[Job]:
    """Query DB for jobs.

    Args:
        query_params (JobGetQueryParams): Query params from request
        user_creds (User): User credentials.

    Raises:
        e: error
        Exception: error

    Returns:
        List[Job]: List of jobs returned from DB
    """
    job_list: List[JobDB] = []

    stmt = ""

    if query_params.query_type == JobQueryType.GET_ALL_JOBS:
        stmt = select(JobDB).where(JobDB.protagonist_id == user_creds.user_id)
    if query_params.query_type == JobQueryType.GET_JOBS_BY_ID:
        if query_params.job_id is None:
            e = ValidationError(
                errors=[
                    ErrorWrapper(ValueError("field required"), "job_id"),
                ],
                model=JobGetQueryParams,
            )
            raise e
        stmt = (
            select(JobDB)
            .where(JobDB.protagonist_id == user_creds.user_id)
            .where(JobDB.id == query_params.job_id)
        )
    if query_params.query_type == JobQueryType.GET_JOBS_BY_CLUSTER_ID:
        if query_params.cluster_id is None:
            e = ValidationError(
                errors=[
                    ErrorWrapper(ValueError("field required"), "cluster_id"),
                ],
                model=JobGetQueryParams,
            )
            raise e
        stmt = (
            select(JobDB)
            .where(JobDB.protagonist_id == user_creds.user_id)
            .where(JobDB.id == query_params.cluster_id)
        )
    if query_params.query_type == JobQueryType.GET_JOBS_BY_PROTAGONIST_ID:
        stmt = select(JobDB).where(JobDB.protagonist_id == user_creds.user_id)
    if query_params.query_type == JobQueryType.GET_JOBS_BY_STATUS:
        if query_params.job_status is None:
            e = ValidationError(
                errors=[
                    ErrorWrapper(ValueError("field required"), "job_status"),
                ],
                model=JobGetQueryParams,
            )
            raise e
        stmt = (
            select(JobDB)
            .where(JobDB.protagonist_id == user_creds.user_id)
            .where(JobDB.id == query_params.job_status)
        )

    with DBSession() as session:
        try:
            job_db_list: List[JobDB] = session.execute(stmt).scalars().all()
            job_list = [Job(job_id=obj.id, **obj.to_dict()) for obj in job_db_list]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch jobs due to {e}")
            raise e

    return job_list


def update_job(job_update_list: List[JobUpdate], user_creds: User) -> List[Job]:
    """Update job in the DB from JobUpdate request.

    Args:
        job_update_list (List[JobUpdate]): List of JobUpdate request
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        List[Job]: List of Instance of Updated Job
    """
    stmt = (
        select(JobDB)
        .where(JobDB.protagonist_id == user_creds.user_id)
        .where(JobDB.id.in_([job_update.template_id for job_update in job_update_list]))
    )
    with DBSession() as session:
        try:
            job_db_update_list: List[JobDB] = session.execute(stmt).scalars().all()
            updated_job_list = []
            for job in job_db_update_list:
                for job_update in job_update_list:
                    if job_update.job_id == job.id:
                        job_update_dict = job_update.dict(exclude_defaults=True)
                        job_update_dict.pop("job_id")
                        updated_job = job.update(session, **job_update_dict)
                        updated_job_list.append(
                            Job(
                                job_id=updated_job.id,
                                **updated_job.to_dict(),
                            )
                        )
            return updated_job_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to update job: {job.to_dict()} due to {e}")
            raise e


def delete_job(job_delete_list: List[JobDelete], user_creds: User) -> List[Job]:
    """Delete job in the DB from JobDelete request.

    Args:
        job_delete_list (List[JobDelete]): List of JobDelete request
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        List[Job]: List of Instance of Deleted Job
    """
    stmt = (
        select(JobDB)
        .where(JobDB.protagonist_id == user_creds.user_id)
        .where(JobDB.id.in_([job.job_id for job in job_delete_list]))
    )
    with DBSession() as session:
        try:
            job_db_delete_list: List[JobDB] = session.execute(stmt).scalars().all()
            deleted_job_list = []
            for job in job_db_delete_list:
                job.delete(session)
                deleted_job_list.append(Job(job_id=job.id, **job.to_dict()))
            return deleted_job_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to delete job: {job.to_dict()} due to {e}")
            raise e


###
# Flow BLoCs
###


def check_job_list_exist(inputs: List[Prop]) -> List[Prop]:
    """Check data list exist step.

    Args:
        inputs (List[Prop]):
            Expects
                0: job_id_list
                    Prop(data=job_id_list, description="List of ids of job objects")
                1: user
                    Prop(data=user, description="User")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:

            Prop(data=job_list, description="List of job Objects ids")
    """
    try:
        job_id_list: List[str] = inputs[0].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        # Check job list existence
        job_query = JobGetQueryParams(query_type=JobQueryType.GET_ALL_JOBS)
        job_list: List[Job] = get_job(job_query, user)
        job_list_ids = [str(job.job_id) for job in job_list]
        # Use sets to optimize later
        for job_id in job_id_list:
            if job_id not in job_list_ids:
                # Raise a user descriptive error later
                raise Exception("JOB NOT FOUND")

    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Querying DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=job_list, description="List of job Objects"),
    ]


def create_job_db_entry(inputs: List[Prop]) -> List[Prop]:
    """Forward function for create db entry step.

    Args:
        inputs (List[Prop]):
            Expects
                0: job_create_request_list
                    Prop(data=job_create_request_list, description="List of create job objects")
                2: user
                    Prop(data=user, description="User")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Created job objects

            Prop(data=created_job_list, description="List of created job Objects")
    """
    try:
        job_create_request_list: List[JobCreate] = inputs[0].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        created_job_list = create_job(job_create_request_list, user)
    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Creating DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=created_job_list, description="List of created job Objects"),
        Prop(data=user, description="User"),
    ]


def revert_job_db_entry(inputs: List[Prop]) -> List[Prop]:
    """Revert function for create db entry step.

    Args:
        inputs (List[Prop]):
            Expects
                0: job_create_request_list
                    Prop(data=job_create_request_list, description="List of create job objects")
                1: user
                    Prop(data=user, description="User")
                2: created_job_list
                    Prop(data=created_job_list, description="List of created job objects")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Deleted job objects

            Prop(data=deleted_job_list, description="List of deleted job Objects")
    """
    try:
        created_job_list: List[Job] = inputs[2].data
        user: User = inputs[3].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        deleted_job_list = delete_job(created_job_list, user)
    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Deleting DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=deleted_job_list, description="List of deleted job Objects"),
        Prop(data=user, description="User"),
    ]
