"""Blackcap Cluster DELETE route schemas."""

from typing import Any, Dict, List, Union

from pydantic import BaseModel
from pydantic.types import UUID4


from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.cluster import Cluster


class ClusterDelete(BaseModel):
    """Schema to parse delete cluster requests."""

    cluster_id: UUID4


class ClusterPUTRequest(BaseModel):
    """Cluster PUT request schema."""

    cluster_list: List[ClusterDelete]


class ClusterPUTResponse(ResponseSchema):
    """Cluster PUT response schema."""

    items: Dict[str, List[Union[Cluster, Any]]] = {}
