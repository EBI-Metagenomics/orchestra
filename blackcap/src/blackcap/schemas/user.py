"""User schema."""

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class User(BaseModel):
    """User schema."""

    user_id: Optional[UUID4]
    name: str
    organisation: str
    email: str
    active: bool = True
