"""Conductor Schedule POST route schemas."""

from typing import List, Optional

from conductor.schemas.schedule import Schedule
from conductor.schemas.user import User

from pydantic import BaseModel


class SchedulePOSTResponse(BaseModel):
    """Schedule POST response schema."""

    items: List[Schedule] = []


class ScheduleCreate(BaseModel):
    """Schema to parse create schedule requests."""

    schedule: Schedule
    user: Optional[User]


class SchedulePOSTRequest(BaseModel):
    """Schedule POST request schema."""

    schedules: List[ScheduleCreate]
