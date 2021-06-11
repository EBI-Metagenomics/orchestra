"""Conductor extensions."""

from typing import Any

from celery import Celery

from flask import Flask

celery_app = Celery(__name__)


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
