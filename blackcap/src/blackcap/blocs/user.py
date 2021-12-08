"""User BLoCs."""

from typing import List

from blackcap.configs import config_registry
from blackcap.db import DBSession
from blackcap.auther import auther_registry
from blackcap.models.protagonist import ProtagonistDB
from blackcap.schemas.api.user.delete import UserDelete
from blackcap.schemas.api.user.get import UserGetQueryParams, UserQueryType
from blackcap.schemas.api.user.post import UserCreate
from blackcap.schemas.api.user.put import UserUpdate
from blackcap.schemas.user import User

from logzero import logger

from sqlalchemy import select


config = config_registry.get_config()
auther = auther_registry.get_auther(config.AUTHER)


def create_user(user_create_list: List[UserCreate]) -> List[User]:
    """Create user and save to DB from UserCreate request.

    Args:
        user_create_list (List[UserCreate]): List of UserCreate request

    Raises:
        Exception: error

    Returns:
        List[User]: Created user
    """
    try:
        user_list = auther.register_user(user_create_list)
        return user_list
    except Exception as e:
        logger.error(f"Unable to register users due to {e}")
        raise e


def get_users(query_params: UserGetQueryParams) -> List[User]:
    """Query DB for users.

    Args:
        query_params (UserGetQueryParams): User Query params

    Raises:
        Exception: error

    Returns:
        List[User]: List of Users
    """
    user_list: List[ProtagonistDB] = []

    if query_params.query_type == UserQueryType.GET_ALL_USERS:
        stmt = select(ProtagonistDB)
    if query_params.query_type == UserQueryType.GET_USER_BY_ID:
        stmt = select(ProtagonistDB).where(
            ProtagonistDB.id == query_params.user_id
        )  # noqa: E501
    if query_params.query_type == UserQueryType.GET_USERS_BY_EMAIL:
        stmt = select(ProtagonistDB).where(
            ProtagonistDB.email == query_params.email
        )  # noqa: E501
    if query_params.query_type == UserQueryType.GET_USERS_BY_ORGANISATION:
        stmt = select(ProtagonistDB).where(
            ProtagonistDB.organisation == query_params.organisation
        )

    with DBSession() as session:
        try:
            user_list: List[ProtagonistDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            user_list = [
                User(user_id=obj.id, **obj.to_dict()) for obj in user_list
            ]  # noqa: E501
            return user_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch users due to {e}")
            raise e


def update_user(user_update: UserUpdate) -> User:
    """Update user in the DB from UserUpdate request.

    Args:
        user_update (UserUpdate): User update request

    Returns:
        User: Instance of updated user
    """
    stmt = select(ProtagonistDB).where(ProtagonistDB.id == user_update.user_id)
    with DBSession() as session:
        try:
            user_list: List[ProtagonistDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            if not user_list:
                # TODO: raise not found error
                pass
            if len(user_list) == 1:
                user_update_dict = user_update.dict(exclude_defaults=True)
                user_update_dict.pop("user_id")
                updated_user = user_list[0].update(
                    session, **user_update_dict
                )  # noqa: E501
                return User(user_id=updated_user.id, **updated_user.to_dict())
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to update user: {user_update.dict()} due to {e}"
            )  # noqa: E501
            # TODO: Raise error


def delete_user(user_delete: UserDelete) -> User:
    """Delete user in the DB from UserDelete request.

    Args:
        user_delete (UserDelete): User delete request

    Raises:
        Exception: error

    Returns:
        User: Instance of deleted user
    """
    stmt = select(ProtagonistDB).where(ProtagonistDB.id == user_delete.user_id)
    with DBSession() as session:
        try:
            user_list: List[ProtagonistDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            if not user_list:
                # TODO: raise not found error
                pass
            if len(user_list) == 1:
                deleted_user = user_list[0].delete(session)
                return User(user_id=deleted_user.id, **deleted_user.to_dict())
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to delete user: {user_delete.dict()} due to {e}"
            )  # noqa: E501
            raise e
