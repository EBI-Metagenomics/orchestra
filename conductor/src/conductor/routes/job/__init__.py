"""Conductor job routes."""

from flask import Blueprint


job_bp = Blueprint("job", __name__, url_prefix="/v1/job")


from conductor.routes.job.get import get_job  # noqa: F401, E402, I100
from conductor.routes.job.post import post_job  # noqa: F401, E402, I100
