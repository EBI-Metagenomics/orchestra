"""User BLoCs integration tests."""
# flake8: noqa

from typing import Dict
from conductor.blocs.user import create_user, delete_user, get_users, update_user
from conductor.models.protagonist import ProtagonistDB
from conductor.schemas.api.user.get import UserGetQueryParams, UserQueryType
from conductor.schemas.api.user.post import UserCreate
from conductor.schemas.user import User

from logzero import logger

from sqlalchemy import select
from sqlalchemy.orm.session import Session


def test_create_user_bloc(db: Session) -> None:
    create_user_list = [
        UserCreate(
            user=User(
                name="tony stark",
                organisation="stark industries",
                email="tony@stark.com",
            ),
            password="IAMaPASS",
        )
    ]
    created_user_list = create_user(create_user_list)
    with db() as session:
        stmt = select(ProtagonistDB)
        try:
            fetched_users = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(f"Unable tofetch user: {e}")
            raise e
        assert "tony@stark.com" in [str(u.email) for u in fetched_users]


def test_get_all_user_bloc(user_dict: Dict) -> None:
    query_params = UserGetQueryParams(query_type=UserQueryType.GET_ALL_USERS)
    returned_users = get_users(query_params)
    assert user_dict["id"] in [str(u.id) for u in returned_users]
