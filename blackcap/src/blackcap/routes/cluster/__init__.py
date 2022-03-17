"""Blackcap cluster routes."""

from flask import Blueprint


cluster_bp = Blueprint("cluster", __name__, url_prefix="/v1/cluster")


from blackcap.routes.cluster.get import get  # noqa: F401, E402, I100
from blackcap.routes.cluster.post import post  # noqa: F401, E402, I100
