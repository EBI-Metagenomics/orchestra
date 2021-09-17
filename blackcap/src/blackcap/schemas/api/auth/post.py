"""Blackcap Auth POST route schemas."""

from typing import List

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User

from pydantic import BaseModel


class AuthUserCreds(BaseModel):
    """Schema to parse User credentials."""

    email: str
    password: str


class AuthPOSTResponse(ResponseSchema):
    """User POST response schema."""

    items: List[User] = []
