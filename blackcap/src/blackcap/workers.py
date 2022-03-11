"""Blackcap workers."""

from celery import Celery

from blackcap.configs import config_registry

celery_app = Celery(
    __name__,
    broker=config_registry.get_config().CELERY_BROKER_URL,
    backend=config_registry.get_config().CELERY_RESULT_BACKEND,
    include=["blackcap.tasks"],
)

celery_app.conf.task_routes = {"blackcap.tasks.*": {"queue": "blackcap"}}
