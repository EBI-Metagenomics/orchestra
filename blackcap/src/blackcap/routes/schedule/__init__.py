"""Blackcap schedule routes."""


from flask import Blueprint

schedule_bp = Blueprint("schedule", __name__, url_prefix="/v1/schedule")

from conductor.routes.schedule.get import get_schedule  # noqa: F401, E402, I100, E501

# from conductor.routes.schedule.post import post_schedule  # noqa: F401, E402, I100, E501
