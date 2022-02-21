"""Blackcap User POST route schemas."""

from typing import Any, Dict, List, Union

from pydantic import BaseModel

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User


class UserCreate(BaseModel):
    """Schema to parse create User requests."""

    user: User
    password: str


class UserPOSTRequest(BaseModel):
    """User POST request schema."""

    users: List[UserCreate]


class UserPOSTResponse(ResponseSchema):
    """User POST response schema."""

    items: Dict[str, List[Union[User, Any]]] = {}
