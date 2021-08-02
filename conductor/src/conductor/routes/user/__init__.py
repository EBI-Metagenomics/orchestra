"""Conductor user routes."""

from flask import Blueprint

user_bp = Blueprint("user", __name__, url_prefix="/v1/user")
