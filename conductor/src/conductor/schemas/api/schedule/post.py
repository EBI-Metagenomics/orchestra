"""Conductor Schedule POST route schemas."""

from typing import Optional

from conductor.schemas.schedule import Schedule
from conductor.schemas.user import User

from pydantic import BaseModel


class SchedulePOSTRequest(BaseModel):
    """Schedule POST request schema."""

    pass


class SchedulePOSTResponse(BaseModel):
    """Schedule POST response schema."""

    pass


class ScheduleCreate(BaseModel):
    """Schema to parse create schedule requests."""

    schedule: Schedule
    user: Optional[User]
