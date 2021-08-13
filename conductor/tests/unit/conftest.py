"""Conductor conftest."""

from typing import Generator

from conductor import db_engine
from conductor.models.meta.mixins import DBModel

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
