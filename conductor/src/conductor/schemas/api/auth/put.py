"""Conductor Auth PUT route schemas."""
from typing import List

from conductor.schemas.api.common import ResponseSchema
from conductor.schemas.user import User

from pydantic import BaseModel


class AuthCredsUpdate(BaseModel):
    """Schema to parse update user creds requests."""

    update_token: str
    new_password: str


class AuthPOSTResponse(ResponseSchema):
    """User POST response schema."""

    items: List[User]
