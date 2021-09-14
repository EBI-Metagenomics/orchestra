"""Blackcap user routes."""


from flask import Blueprint

user_bp = Blueprint("user", __name__, url_prefix="/v1/user")

from blackcap.routes.user.get import get_user  # noqa: F401, E402, I100
from blackcap.routes.user.post import post_user  # noqa: F401, E402, I100
