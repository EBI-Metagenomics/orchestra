"""Blackcap User POST route schemas."""

from typing import List

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema to parse create User requests."""

    user: User
    password: str


class UserPOSTRequest(BaseModel):
    """User POST request schema."""

    users: List[UserCreate]


class UserPOSTResponse(ResponseSchema):
    """User POST response schema."""

    items: List[User] = []
