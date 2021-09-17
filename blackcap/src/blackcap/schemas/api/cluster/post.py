"""Blackcap Cluster POST route schemas."""

from typing import List, Optional

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.cluster import Cluster
from blackcap.schemas.user import User

from pydantic import BaseModel


class ClusterCreate(BaseModel):
    """Schema to parse create Cluster requests."""

    cluster: Cluster
    user: Optional[User]


class ClusterPOSTRequest(BaseModel):
    """Cluster POST request schema."""

    Clusters: List[ClusterCreate]


class ClusterPOSTResponse(ResponseSchema):
    """Cluster POST response schema."""

    items: List[Cluster] = []
