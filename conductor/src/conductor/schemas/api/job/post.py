"""Conductor Job POST route schemas."""

from typing import List, Optional

from conductor.schemas.job import Job
from conductor.schemas.user import User

from pydantic import BaseModel


class JobPOSTResponse(BaseModel):
    """Job POST response schema."""

    items: List[Job] = []


class JobCreate(BaseModel):
    """Schema to parse create job requests."""

    job: Job
    user: Optional[User]


class JobPOSTRequest(BaseModel):
    """Job POST request schema."""

    jobs: List[JobCreate]
