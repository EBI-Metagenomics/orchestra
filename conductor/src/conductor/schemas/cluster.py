"""Cluster schema."""

from typing import Optional

from pydantic import BaseModel


class Cluster(BaseModel):
    """Cluster schema."""

    name: str
    cluster_type: str
    status: str
    cluster_caps: Optional[str]
    messenger: str
    messenger_queue: str
