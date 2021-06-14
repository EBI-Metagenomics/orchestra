"""Conductor extensions."""

from typing import Any

from celery import Celery

from conductor.configs import get_config

from flask import Flask

default_config = get_config()
celery_app = Celery(
    __name__,
    broker=default_config.CELERY_BROKER_URL,
    backend=default_config.CELERY_RESULT_BACKEND,
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
