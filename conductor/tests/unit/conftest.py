"""Conductor conftest."""

from typing import Generator

from bcrypt import gensalt, hashpw


from conductor import db_engine
from conductor.models.meta.mixins import DBModel
from conductor.models.protagonist import ProtagonistDB

from logzero import logger

import pytest

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


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
def user() -> ProtagonistDB:
    """User from the DB.

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

    return user
