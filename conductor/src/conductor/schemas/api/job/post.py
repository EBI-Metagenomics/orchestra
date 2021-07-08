"""Conductor Job POST route schemas."""

from pydantic import BaseModel


class JobPOSTRequest(BaseModel):
    """Job POST request schema."""

    pass


class JobPOSTResponse(BaseModel):
    """Job POST response schema."""

    pass


class JobCreate(BaseModel):
    """Schema to parse create job requests."""

    pass
