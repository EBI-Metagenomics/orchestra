"""Blackcap User PUT route schemas."""

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class UserUpdate(BaseModel):
    """Schema to parse update user requests."""

    user_id: UUID4
    name: Optional[str]
    email: Optional[str]
    organisation: Optional[str]
