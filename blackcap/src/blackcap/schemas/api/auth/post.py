"""Auth API POST schema."""

from typing import Any, Dict, List, Union

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User
from pydantic import BaseModel


class AuthPOSTResponse(ResponseSchema):
    """Auth POST response schema."""

    items: Dict[str, List[Union[User, Any]]] = []


class AuthPOSTRequest(BaseModel):
    """Auth POST request schema."""

    email: str
    password: str
