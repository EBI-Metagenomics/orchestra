"""Blackcap Auth DELETE route schemas."""

from pydantic import BaseModel
from pydantic.types import UUID4


class AuthLogout(BaseModel):
    """Schema to parse delete user requests."""

    user_id: UUID4
