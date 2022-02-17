"""Blackcap Auth POST route schemas."""

from typing import Any, Dict, List, Union

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User

from pydantic import BaseModel


class AuthUserCreds(BaseModel):
    """Schema to parse User credentials."""

    email: str
    password: str


class AuthPOSTResponse(ResponseSchema):
    """User POST response schema."""

    items: Dict[str, List[Union[User, Any]]] = {}
