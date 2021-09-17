"""Blackcap Cluster GET route schemas."""

from enum import Enum, unique
from typing import List

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.cluster import Cluster

from pydantic import BaseModel


@unique
class ClusterQueryType(Enum):
    """Cluster Query type enum."""

    GET_ALL_CLUSTER = "get_all_clusters"


class ClusterGetQueryParams(BaseModel):
    """Cluster GET request query params schema."""

    query_type: ClusterQueryType


class ClusterGetResponse(ResponseSchema):
    """Cluster GET response schema."""

    items: List[Cluster] = []
