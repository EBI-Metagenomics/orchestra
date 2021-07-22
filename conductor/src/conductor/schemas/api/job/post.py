"""Conductor Job POST route schemas."""

from conductor.schemas.job import Job

from pydantic import BaseModel


class JobPOSTRequest(BaseModel):
    """Job POST request schema."""

    pass


class JobPOSTResponse(BaseModel):
    """Job POST response schema."""

    pass


class JobCreate(BaseModel):
    """Schema to parse create job requests."""

    job: Job
