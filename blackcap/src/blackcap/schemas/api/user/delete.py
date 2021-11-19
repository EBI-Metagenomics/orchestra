"""Blackcap User DELETE route schemas."""

from typing import List

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User


class UserDelete(BaseModel):
    """Schema to parse delete user requests."""

    user_id: UUID4


class UserDELETEResponse(ResponseSchema):
    """User DELETE response schema."""

    items: List[User] = []
