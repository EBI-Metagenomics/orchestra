"""Cookie Auther implementation of Auther."""


from typing import List

from bcrypt import gensalt, hashpw

from conductor import DBSession
from conductor.auther.base import BaseAuther
from conductor.models.protagonist import ProtagonistDB
from conductor.schemas.api.user.post import UserCreate

from logzero import logger


class CookieAuther(BaseAuther):
    """Cookie Auther."""

    def register_user(
        self: "BaseAuther", user_create_list: List[UserCreate]
    ) -> ProtagonistDB:
        """Register user.

        Args:
            user_create_list (List[UserCreate]): List of users to register

        Returns:
            List(ProtagonistDB): List of registered users
        """
        with DBSession() as session:
            try:
                ProtagonistDB.bulk_create(
                    [
                        {
                            "password": hashpw(
                                user_create["password"].encode(), gensalt()
                            ),
                            **user_create["user"],
                        }  # noqa: E501
                        for user_create in user_create_list
                    ],
                    session,
                )
                return [
                    {**user_create["user"]} for user_create in user_create_list
                ]  # noqa: E501
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to register users due to {e}")
                raise e

    def login_user(self: "BaseAuther") -> None:
        return super().login_user()

    def logout_user(self: "BaseAuther") -> None:
        return super().logout_user()

    def authorize_user(self: "BaseAuther") -> None:
        return super().authorize_user()
