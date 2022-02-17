"""Blackcap Cluster POST route schemas."""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.cluster import Cluster


class ClusterCreate(BaseModel):
    """Schema to parse create Cluster requests."""

    name: str
    cluster_type: str
    status: str = "ONLINE"
    cluster_caps: Optional[str]
    messenger: str
    messenger_queue: str


class ClusterPOSTRequest(BaseModel):
    """Cluster POST request schema."""

    cluster_list: List[ClusterCreate]


class ClusterPOSTResponse(ResponseSchema):
    """Cluster POST response schema."""

    items: Dict[str, List[Union[Cluster, Any]]] = {}
