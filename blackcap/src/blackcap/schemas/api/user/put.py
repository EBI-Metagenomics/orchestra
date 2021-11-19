"""Blackcap User PUT route schemas."""

from typing import List, Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User


class UserUpdate(BaseModel):
    """Schema to parse update user requests."""

    user_id: UUID4
    name: Optional[str]
    email: Optional[str]
    organisation: Optional[str]


class UserPUTResponse(ResponseSchema):
    """User PUT response schema."""

    items: List[User] = []
