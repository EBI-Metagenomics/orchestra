"""Test job BLoCs."""
# flake8: noqa

from typing import Dict

from blackcap.blocs.job import create_job, delete_job, get_job, update_job
from blackcap.models.job import JobDB
from blackcap.schemas.api.job.delete import JobDelete
from blackcap.schemas.api.job.get import JobGetQueryParams, JobQueryType
from blackcap.schemas.api.job.post import JobCreate
from blackcap.schemas.api.job.put import JobUpdate
from blackcap.schemas.job import Job
from blackcap.schemas.user import User

from logzero import logger

from sqlalchemy import select
from sqlalchemy.orm.session import Session


def test_job_create_bloc(user: User) -> None:
    create_job_request = JobCreate(
        name="cool_job",
        description="job desc",
        script=" #! /bin/bash\n\n/bin/hostname\nsrun -l /bin/hostname\nsrun -l /bin/hostname\n",
    )

    created_job = create_job([create_job_request], user)[0]
    assert "cool_job" == created_job.name


def test_get_all_jobs_bloc(job: Job, user: User) -> None:
    query_params = JobGetQueryParams(query_type=JobQueryType.GET_ALL_JOBS)
    returned_jobs = get_job(query_params, user)
    assert job in returned_jobs
