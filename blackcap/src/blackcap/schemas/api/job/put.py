"""Blackcap Job PUT route schemas."""

from pydantic import BaseModel
from pydantic.types import UUID4


class JobUpdate(BaseModel):
    """Schema to parse update job requests."""

    job_id: UUID4
