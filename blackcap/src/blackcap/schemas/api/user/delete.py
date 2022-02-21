"""Blackcap User DELETE route schemas."""

from typing import Any, Dict, List, Union

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User


class UserDelete(BaseModel):
    """Schema to parse delete user requests."""

    user_id: UUID4


class UserDELETEResponse(ResponseSchema):
    """User DELETE response schema."""

    items: Dict[str, List[Union[User, Any]]] = {}
