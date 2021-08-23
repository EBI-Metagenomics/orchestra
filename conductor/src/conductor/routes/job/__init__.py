"""Conductor job routes."""

from conductor.routes.job.get import get_job  # noqa: F401
from conductor.routes.job.post import post_job  # noqa: F401

from flask import Blueprint


job_bp = Blueprint("job", __name__, url_prefix="/v1/job")
