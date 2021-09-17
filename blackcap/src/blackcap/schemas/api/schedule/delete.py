"""Blackcap Schedule DELETE route schemas."""

from pydantic import BaseModel
from pydantic.types import UUID4


class ScheduleDelete(BaseModel):
    """Schema to parse delete schedule requests."""

    schedule_id: UUID4
