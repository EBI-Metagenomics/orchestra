"""Blackcap Cluster PUT route schemas."""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.cluster import Cluster


class ClusterUpdate(BaseModel):
    """Schema to parse update cluster requests."""

    cluster_id: UUID4
    cluster_type: Optional[str]
    cluster_caps: Optional[str]
    messenger: Optional[str]
    messenger_queue: Optional[str]


class ClusterPUTRequest(BaseModel):
    """Cluster PUT request schema."""

    cluster_list: List[ClusterUpdate]


class ClusterPUTResponse(ResponseSchema):
    """Cluster PUT response schema."""

    items: Dict[str, List[Union[Cluster, Any]]] = {}
