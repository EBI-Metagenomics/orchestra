"""Blackcap Cluster PUT route schemas."""

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class ClusterUpdate(BaseModel):
    """Schema to parse update cluster requests."""

    cluster_id: UUID4
    cluster_type: Optional[str]
    cluster_caps: Optional[str]
    messenger: Optional[str]
    messenger_queue: Optional[str]
