"""Conductor job routes."""
from flask import Blueprint

job_bp = Blueprint("job", __name__, url_prefix="/v1/job")
