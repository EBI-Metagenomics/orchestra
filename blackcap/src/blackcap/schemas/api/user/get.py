"""Blackcap User GET route schemas."""

from enum import Enum, unique
from typing import List, Optional

from pydantic import BaseModel

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User


@unique
class UserQueryType(Enum):
    """User Query type enum."""

    GET_ALL_USERS = "get_all_users"
    GET_USER_BY_ID = "get_user_by_id"
    GET_USERS_BY_EMAIL = "get_users_by_email"
    GET_USERS_BY_ORGANISATION = "get_users_by_organisation"


class UserGetQueryParams(BaseModel):
    """User GET request query params schema."""

    query_type: UserQueryType
    user_id: Optional[str]
    email: Optional[str]
    organisation: Optional[str]


class UserGetResponse(ResponseSchema):
    """User GET response schema."""

    items: List[User] = []
