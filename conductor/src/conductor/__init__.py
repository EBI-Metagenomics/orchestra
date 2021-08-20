"""Conductor."""

from importlib.metadata import PackageNotFoundError, version  # type: ignore

from conductor.configs import get_config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

# Initialize global config
global_config = get_config()


db_engine = create_engine(global_config.get_sql_db_uri())
# Use this session for all db operations in the app
DBSession = sessionmaker(db_engine)
