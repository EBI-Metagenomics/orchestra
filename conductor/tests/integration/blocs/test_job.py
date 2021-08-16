"""Test job BLoCs."""
# flake8: noqa

from typing import Dict

from conductor.blocs.job import create_job, delete_job, get_jobs, update_job
from conductor.models.job import JobDB
from conductor.schemas.api.job.delete import JobDelete
from conductor.schemas.api.job.get import JobGetQueryParams, JobQueryType
from conductor.schemas.api.job.post import JobCreate
from conductor.schemas.api.job.put import JobUpdate
from conductor.schemas.job import Job
from conductor.schemas.user import User

from logzero import logger

from sqlalchemy import select
from sqlalchemy.orm.session import Session


def test_job_create_bloc(user_dict: Dict, db: Session) -> None:
    job = Job(
        name="cool_job",
        script="#! /bin/bash\n\n/bin/hostname\nsrun -l /bin/hostname\nsrun -l /bin/hostname\n",
    )

    user = User(**user_dict)

    create_job_request = JobCreate(job=job, user=user)

    created_jobs = create_job([create_job_request])
    with db() as session:
        stmt = select(JobDB)
        try:
            fetched_jobs = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(f"Unable to fetch jobs: {e}")
            raise e
        assert "cool_job" in [str(j.name) for j in fetched_jobs]


def test_get_all_jobs_bloc(job_dict: Dict) -> None:
    query_params = JobGetQueryParams(query_type=JobQueryType.GET_ALL_JOBS)
    returned_jobs = get_jobs(query_params)
    assert job_dict["id"] in [str(j.id) for j in returned_jobs]
