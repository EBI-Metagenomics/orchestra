"""Demon's celery interface."""

from demon.cluster import get_cluster
from demon.messenger import get_messenger


messenger = get_messenger()
cluster = get_cluster()
