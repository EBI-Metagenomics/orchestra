"""Job schema unit tests."""
# flake8: noqa

import json
from uuid import uuid4

from blackcap.schemas.job import Job


def test_job_schema_create() -> None:
    job_uuid = uuid4()
    job = Job(job_id=job_uuid, name="bio job", script="#!/bin/bash")
    assert job.job_id == job_uuid
    assert job.name == "bio job"
    assert job.script == "#!/bin/bash"


def test_job_schema_to_dict() -> None:
    job_uuid = uuid4()
    job = Job(job_id=job_uuid, name="bio job", script="#!/bin/bash")
    job_dict = job.dict()
    assert job_dict["job_id"] == job_uuid
    assert job_dict["name"] == "bio job"
    assert job_dict["script"] == "#!/bin/bash"


def test_job_schema_to_json() -> None:
    job_uuid = uuid4()
    job = Job(job_id=job_uuid, name="bio job", script="#!/bin/bash")
    job_json = job.json()
    job_dict = json.loads(job_json)
    assert job_dict["job_id"] == str(job_uuid)
    assert job_dict["name"] == "bio job"
    assert job_dict["script"] == "#!/bin/bash"
