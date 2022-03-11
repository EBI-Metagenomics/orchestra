"""Blackcap Schedule POST route schemas."""

from typing import Any, Dict, List, Optional, Union

from blackcap.schemas.schedule import Schedule

from pydantic import BaseModel, UUID4


class ScheduleCreate(BaseModel):
    """Schema to parse create schedule requests."""

    job_id: UUID4
    assigned_cluster_id: Optional[UUID4]
    messenger: Optional[str]
    messenger_queue: Optional[str]
    status: str = "PENDING"


class SchedulePOSTRequest(BaseModel):
    """Schedule POST request schema."""

    schedule_list: List[ScheduleCreate]


class SchedulePOSTResponse(BaseModel):
    """Schedule POST response schema."""

    items: Dict[str, List[Union[Schedule, Any]]] = {}
