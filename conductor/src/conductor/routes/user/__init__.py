"""Conductor user routes."""

from conductor.routes.user.get import get_user  # noqa: F401
from conductor.routes.user.post import post_user  # noqa: F401

from flask import Blueprint

user_bp = Blueprint("user", __name__, url_prefix="/v1/user")
