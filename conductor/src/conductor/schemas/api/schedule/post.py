"""Conductor Schedule POST route schemas."""

from conductor.schemas.schedule import Schedule

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
