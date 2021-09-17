"""Blackcap Cluster DELETE route schemas."""

from pydantic import BaseModel
from pydantic.types import UUID4


class ClusterDelete(BaseModel):
    """Schema to parse delete cluster requests."""

    cluster_id: UUID4
