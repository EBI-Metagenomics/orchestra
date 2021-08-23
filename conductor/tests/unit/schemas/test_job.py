"""Job schema unit tests."""
# flake8: noqa

from uuid import uuid4

from conductor.schemas.job import Job


def test_job_schema_create() -> None:
    job_uuid = uuid4()
    job = Job(job_id=job_uuid, name="bio jo", script="#!/bin/bash")
    assert job.job_id == job_uuid
    assert job.name == "bio job"
    assert job.script == "#!/bin/bash"


def test_job_schema_to_dict() -> None:
    job_uuid = uuid4()
    job = Job(job_id=job_uuid, name="bio jo", script="#!/bin/bash")
    job_dict = job.dict()
    assert job["job_id"] == job_uuid
    assert job_dict["name"] == "bio job"
    assert job_dict["script"] == "#!/bin/bash"


def test_job_schema_to_json() -> None:
    job_uuid = uuid4()
    job = Job(job_id=job_uuid, name="bio jo", script="#!/bin/bash")
    job_dict = job.json()
    assert job_dict["job_id"] == job_uuid
    assert job_dict["name"] == "bio job"
    assert job_dict["script"] == "#!/bin/bash"
