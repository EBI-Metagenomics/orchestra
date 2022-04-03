"""User BLoCs integration tests."""
# flake8: noqa

from typing import Dict
from blackcap.blocs.user import create_user, delete_user, get_users, update_user
from blackcap.models.protagonist import ProtagonistDB
from blackcap.schemas.api.user.get import UserGetQueryParams, UserQueryType
from blackcap.schemas.api.user.post import UserCreate
from blackcap.schemas.user import User

from logzero import logger

from sqlalchemy import select
from sqlalchemy.orm.session import Session


def test_create_user_bloc() -> None:
    create_user_list = [
        UserCreate(
            user=User(
                name="tony stark",
                organisation="stark industries",
                email="bruce@stark.com",
            ),
            password="IAMaPASS",
        )
    ]
    created_user_list = create_user(create_user_list)
    assert created_user_list[0].email == create_user_list[0].user.email


def test_get_all_user_bloc(user: User) -> None:
    query_params = UserGetQueryParams(query_type=UserQueryType.GET_ALL_USERS)
    returned_users = get_users(query_params)
    assert user in returned_users
