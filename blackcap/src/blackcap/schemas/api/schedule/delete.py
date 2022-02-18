"""Blackcap Schedule DELETE route schemas."""

from typing import Any, Dict, List, Union

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.schedule import Schedule


class ScheduleDelete(BaseModel):
    """Schema to parse delete schedule requests."""

    schedule_id: UUID4


class SchedulePUTRequest(BaseModel):
    """Schedule PUT request schema."""

    schedule_list: List[ScheduleDelete]


class SchedulePUTResponse(BaseModel):
    """Schedule PUT response schema."""

    items: Dict[str, List[Union[Schedule, Any]]] = {}
