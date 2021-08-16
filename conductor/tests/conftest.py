"""Conductor conftest."""

from typing import Dict, Generator

from bcrypt import gensalt, hashpw


from conductor import db_engine, global_config
from conductor.models.cluster import ClusterDB
from conductor.models.job import JobDB
from conductor.models.meta.mixins import DBModel
from conductor.models.protagonist import ProtagonistDB
from conductor.server import create_app

from flask import Flask

from logzero import logger

import pytest

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


@pytest.fixture(scope="session")
def app() -> Flask:
    """Flask app.

    Returns:
        Flask: Instance of flask app
    """
    app = create_app(global_config)
    app.testing = True
    return app


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    """Databse session object.

    Raises:
        Exception: error

    Yields:
        Iterator[Session]: [description]
    """
    try:
        DBModel.metadata.drop_all(db_engine)
    except Exception as e:
        logger.error(f"fail to drop tables: {e}")

    try:
        DBModel.metadata.create_all(db_engine)
    except Exception as e:
        logger.error(f"fail to create tables: {e}")

    yield sessionmaker(db_engine, expire_on_commit=False)

    try:
        DBModel.metadata.drop_all(db_engine)
    except Exception:
        raise Exception("Unable to clean up Database")


@pytest.fixture(scope="session")
def user_dict(db: Session) -> ProtagonistDB:
    """User from the DB.

    Args:
        db(Session): SQLAlchemy Session

    Returns:
        ProtagonistDB: Instance of ProtagonistDB.
    """
    passwd = hashpw("random_key".encode(), gensalt())
    user = ProtagonistDB(
        name="Bruce Wayne",
        email="bruce@wayne.com",
        password=passwd,
        organisation="Justice League",
    )
    with db() as session:
        user.save(session)
        return user.to_dict()


@pytest.fixture(scope="session")
def cluster_dict(db: Session) -> ClusterDB:
    """Cluster from the DB.

    Args:
        db(Session): SQLAlchemy Session

    Returns:
        ClusterDB: Instance of ClusterDB.
    """
    cluster = ClusterDB(
        name="EBI_Embassy",
        cluster_type="SLURM",
        status="ACTIVE",
        cluster_caps="CPU,GPU",
        messenger="GCP",
        messenger_queue="test-topic",
    )
    with db() as session:
        cluster.save(session)
        return cluster.to_dict()


@pytest.fixture(scope="session")
def job_dict(user_dict: Dict, db: Session) -> JobDB:
    """Job from the DB.

    Args:
        user_dict (Dict): A User dict
        db(Session): SQLAlchemy Session

    Returns:
        JobDB: Instance of JobDB.
    """
    job = JobDB(
        name="demo job",
        script="#! /bin/bash\n\n/bin/hostname\nsrun -l /bin/hostname\nsrun -l /bin/hostname\n",  # noqa: E501
        cluster_caps_req="CPU",
        protagonist_id=user_dict["id"],
    )
    with db() as session:
        job.save(session)
        return job.to_dict()
