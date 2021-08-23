"""Conductor schedule routes."""

from conductor.routes.schedule.get import get_schedule  # noqa: F401
from conductor.routes.schedule.post import post_schedule  # noqa: F401

from flask import Blueprint

schedule_bp = Blueprint("schedule", __name__, url_prefix="/v1/schedule")
