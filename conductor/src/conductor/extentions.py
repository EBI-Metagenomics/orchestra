"""Conductor extensions."""

from typing import Any

from celery import Celery

from conductor import global_config

from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_engine = create_engine(global_config.get_sql_db_uri())
# Use this session for all db operations in the app
DBSession = sessionmaker(db_engine)

celery_app = Celery(
    __name__,
    broker=global_config.CELERY_BROKER_URL,
    backend=global_config.CELERY_RESULT_BACKEND,
)


def init_celery(app: Flask, celery_app: Celery) -> None:
    """Initialize celery app.

    Args:
        app (Flask): Flask app
        celery_app (Celery): Celery app
    """
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self: "ContextTask", *args: Any, **kwargs: Any) -> Any:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
