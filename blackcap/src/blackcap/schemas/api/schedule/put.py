"""Blackcap Schedule PUT route schemas."""

from pydantic import BaseModel
from pydantic.types import UUID4


class ScheduleUpdate(BaseModel):
    """Schema to parse update schedule requests."""

    schedule_id: UUID4
