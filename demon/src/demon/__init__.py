"""Demon."""

from importlib.metadata import PackageNotFoundError, version

from celery import Celery

from demon.configs import get_config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


default_config = get_config()

db_engine = create_engine(default_config.get_sql_db_uri())
# Use this session for all db operations in the app
DBSession = sessionmaker(db_engine)

celery_app = Celery(
    __name__,
    broker=default_config.CELERY_BROKER_URL,
    backend=default_config.CELERY_RESULT_BACKEND,
)
