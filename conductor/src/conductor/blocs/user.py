"""User BLoCs."""

from typing import List

from conductor import DBSession
from conductor.extentions import auther
from conductor.models.protagonist import ProtagonistDB
from conductor.schemas.api.user.delete import UserDelete
from conductor.schemas.api.user.get import UserGetQueryParams, UserQueryType
from conductor.schemas.api.user.post import UserCreate
from conductor.schemas.api.user.put import UserUpdate

from logzero import logger

from sqlalchemy import select


def create_user(user_create_list: List[UserCreate]) -> List[ProtagonistDB]:
    """Create user and save to DB from UserCreate request.

    Args:
        user_create_list (List[UserCreate]): List of UserCreate request

    Returns:
        List[ProtagonistDB]: Created user
    """
    try:
        user_list = auther.register_user(user_create_list)
        return user_list
    except Exception as e:
        logger.error(f"Unable to register users due to {e}")
        raise e


def get_users(query_params: UserGetQueryParams) -> List[ProtagonistDB]:
    """Query DB for users.

    Args:
        query_params (UserGetQueryParams): User Query params

    Returns:
        List[ProtagonistDB]: List of Users
    """
    user_list: List[ProtagonistDB] = []

    if query_params.query_type == UserQueryType.GET_ALL_USERS:
        stmt = select(ProtagonistDB)
    if query_params.query_type == UserQueryType.GET_USERS_BY_ID:
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
            return user_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch users due to {e}")
            raise e

    return user_list


def update_user(user_update: UserUpdate) -> ProtagonistDB:
    """Update user in the DB from UserUpdate request.

    Args:
        user_update (UserUpdate): User update request

    Returns:
        ProtagonistDB: Instance of updated user
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
                user_update_dict = user_update.dict()
                user_update_dict.pop("user_id")
                updated_user = user_list[0].update(
                    session, **user_update.dict()
                )  # noqa: E501
                return updated_user
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to update user: {user_update.dict()} due to {e}"
            )  # noqa: E501
            # TODO: Raise error


def delete_user(user_delete: UserDelete) -> ProtagonistDB:
    """Delete user in the DB from UserDelete request.

    Args:
        user_delete (UserDelete): User delete request

    Returns:
        ProtagonistDB: Instance of deleted user
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
                return deleted_user
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to delete user: {user_delete.dict()} due to {e}"
            )  # noqa: E501
            raise e
