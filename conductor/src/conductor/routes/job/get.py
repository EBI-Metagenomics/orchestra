"""Conductor job GET route."""

from conductor.routes.job import job_bp

from flask import Response


@job_bp.get("/")
def get_job() -> Response:
    """Get job."""
    pass
