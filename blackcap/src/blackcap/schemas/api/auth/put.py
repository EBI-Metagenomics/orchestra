"""Auth API PUT schema."""
from typing import List, Optional

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User
from pydantic import BaseModel


class AuthPUTRequest(BaseModel):
    """Auth PUT request schema."""

    email: str
    password_reset_token: Optional[str]
    new_password: Optional[str]


class AuthPUTResponse(ResponseSchema):
    """Auth POST response schema."""

    items: List[User] = []
