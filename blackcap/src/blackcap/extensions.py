"""Blackcap extensions."""


from blackcap.messenger import get_messenger
from blackcap.observer import get_observer
from blackcap.scheduler import get_scheduler


# order of initialization is important
messenger = get_messenger()
observer = get_observer()
scheduler = get_scheduler()
