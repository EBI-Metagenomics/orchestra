"""Blackcap conftest."""
from typing import Dict

from flask import Flask
import pytest

from blackcap.blocs.cluster import create_cluster
from blackcap.blocs.job import create_job
from blackcap.blocs.schedule import create_schedule
from blackcap.blocs.user import create_user
from blackcap.db import db_engine
from blackcap.configs import config_registry
from blackcap.models.meta.mixins import DBModel
from blackcap.schemas.api.auth.post import AuthPOSTRequest
from blackcap.schemas.api.cluster.post import ClusterCreate
from blackcap.schemas.api.job.post import JobCreate
from blackcap.schemas.api.schedule.post import ScheduleCreate
from blackcap.schemas.api.user.post import UserCreate
from blackcap.schemas.cluster import Cluster
from blackcap.schemas.job import Job
from blackcap.schemas.schedule import Schedule
from blackcap.schemas.user import User
from blackcap.server import create_app, register_blueprints, register_extensions


config = config_registry.get_config()


@pytest.fixture(scope="session")
def app() -> Flask:
    app = create_app(config, register_extensions, register_blueprints)
    app.testing = True
    return app.test_client()


@pytest.fixture(scope="session", autouse=True)
def reset_database() -> None:
    DBModel.metadata.drop_all(db_engine)
    DBModel.metadata.create_all(db_engine)


@pytest.fixture(scope="session")
def user() -> User:
    user_create = UserCreate(  # noqa: S106
        user=User(name="randomName", email="rand@random.com", organisation="RandomOrg"),
        password="password",
    )
    created_user = create_user([user_create])[0]
    return created_user


@pytest.fixture(scope="module")
def cluster(user: User) -> Cluster:
    cluster_create = ClusterCreate(
        name="EBI_Embassy",
        cluster_type="SLURM",
        status="ACTIVE",
        cluster_caps="CPU,GPU",
        messenger="NATS",
        messenger_queue="test-topic",
    )
    created_cluster = create_cluster(cluster_create, user)
    return created_cluster


@pytest.fixture(scope="module")
def job(user: User) -> Job:
    job_create = JobCreate(
        name="demo job",
        description="demo job desc",
        job_type="script_job",
        script="#! /bin/bash\n\n/bin/hostname\nsrun -l /bin/hostname\nsrun -l /bin/hostname\n",  # noqa: B950
    )
    created_job = create_job(job_create, user)
    return created_job


@pytest.fixture(scope="module")
def schedule(user: User, job: Job, cluster: Cluster) -> Schedule:
    schedule_create = ScheduleCreate(
        job_id=job.job_id,
    )
    created_schedule = create_schedule(schedule_create, user)
    return created_schedule


@pytest.fixture(scope="session")
def cookies(user: User, app: Flask) -> Dict:
    user_login = AuthPOSTRequest(email=user.email, password="password")  # noqa: S106
    app.post("/v1/auth/", json=user_login.dict())
    cookie_list = [cookie for cookie in app.cookie_jar]
    # remove cookies from test client
    app.cookie_jar.clear()
    return cookie_list
