"""Cluster schema."""

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class Cluster(BaseModel):
    """Cluster schema."""

    cluster_id: Optional[UUID4]
    name: str
    cluster_type: str
    status: str = "ONLINE"
    cluster_caps: Optional[str]
    messenger: str
    messenger_queue: str
