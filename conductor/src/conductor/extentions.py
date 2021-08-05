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

# order of initialization is important
auther = get_auther()
messenger = get_messenger()
observer = get_observer()
scheduler = get_scheduler()
