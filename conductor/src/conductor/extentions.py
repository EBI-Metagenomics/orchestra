"""Conductor extensions."""


from celery import Celery

from conductor import global_config
from conductor.auther import get_auther
from conductor.messenger import get_messenger
from conductor.observer import get_observer
from conductor.scheduler import get_scheduler


celery_app = Celery(
    __name__,
    broker=global_config.CELERY_BROKER_URL,
    backend=global_config.CELERY_RESULT_BACKEND,
)

auther = get_auther()
messenger = get_messenger()
scheduler = get_scheduler()
observer = get_observer()
