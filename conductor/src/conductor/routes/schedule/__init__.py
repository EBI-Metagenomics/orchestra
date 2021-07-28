"""Conductor schedule routes."""

from flask import Blueprint

schedule_bp = Blueprint("schedule", __name__, url_prefix="/v1/schedule")
