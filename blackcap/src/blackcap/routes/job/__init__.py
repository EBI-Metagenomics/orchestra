"""Blackcap job routes."""

from flask import Blueprint


job_bp = Blueprint("job", __name__, url_prefix="/v1/job")


from blackcap.routes.job.get import get  # noqa: F401, E402, I100
from blackcap.routes.job.post import post  # noqa: F401, E402, I100
