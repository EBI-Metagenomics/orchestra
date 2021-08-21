"""Demon tasks."""

from demon.tasks.periodic_db import setup_periodic_tasks  # noqa: F401
from demon.tasks.pub_cluster import publish_slurm_job_from_db  # noqa: F401
