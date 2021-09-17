"""Cookie Auther implementation of Auther."""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from bcrypt import checkpw, gensalt, hashpw

from blackcap.db import DBSession
from blackcap.auther.base import BaseAuther
from blackcap.configs import config_registry
from blackcap.models.protagonist import ProtagonistDB
from blackcap.schemas.api.auth.post import AuthUserCreds
from blackcap.schemas.api.user.post import UserCreate
from blackcap.schemas.user import User

from flask.wrappers import Request

import jwt

from logzero import logger

from sqlalchemy import select

config = config_registry.get_config()


class CookieAuther(BaseAuther):
    """Cookie Auther."""

    CONFIG_KEY_VAL = "COOKIE"

    def register_user(
        self: "BaseAuther", user_create_list: List[UserCreate]
    ) -> List[User]:
        """Register user.

        Args:
            user_create_list (List[UserCreate]): List of users to register

        Raises:
            Exception: error

        Returns:
            List(User): List of registered users
        """
        with DBSession() as session:
            try:
                protagonist_objs = [
                    ProtagonistDB(
                        password=hashpw(
                            user_create.password.encode(), gensalt()
                        ),  # noqa:E501
                        **user_create.user.dict(exclude={"user_id"}),
                    )
                    for user_create in user_create_list
                ]
                ProtagonistDB.bulk_create(protagonist_objs, session)
                return [
                    User(user_id=obj.id, **obj.to_dict())
                    for obj in protagonist_objs  # noqa: E501
                ]
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to register users due to {e}")
                raise e

    def login_user(
        self: "BaseAuther", user_creds: AuthUserCreds
    ) -> Optional[Tuple[User, str]]:
        """Login user.

        Args:
            user_creds (AuthUserCreds): user creds

        Raises:
            Exception: error

        Returns:
            Optional[Tuple[User, str]]: Tuple containing user and cookie or None  # noqa: E501
        """
        with DBSession() as session:
            try:
                # Find user
                stmt = select(ProtagonistDB).where(
                    ProtagonistDB.email == user_creds.email
                )
                user_list: List[ProtagonistDB] = (
                    session.execute(stmt).scalars().all()
                )  # noqa: E501
                # return early if user not found
                if len(user_list) == 0:
                    return None

                # Check password hash
                if checkpw(
                    user_creds.password.encode(), user_list[0].password
                ):  # noqa: E501
                    # Create cookie and return user and cookie
                    user_cookie = jwt.encode(
                        {
                            "exp": datetime.utcnow()
                            + timedelta(
                                minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES  # noqa: E501
                            ),
                            "sub": user_list[0].email,
                            "email": user_list[0].email,
                            "name": user_list[0].name,
                            "organisation": user_list[0].organisation,
                        },
                        config.SECRET_KEY,
                    )
                    return (
                        User(
                            user_id=user_list[0].id, **user_list[0].to_dict()
                        ),  # noqa: E501
                        user_cookie,
                    )
                else:
                    return None
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to login user due to: {e}")
                raise e

    def logout_user(self: "BaseAuther") -> None:
        """Logout user."""
        pass

    def extract_user_from_token(
        self: "BaseAuther", token: str
    ) -> Optional[User]:  # noqa: E501
        """Extract user from token.

        Args:
            token (str): user access token

        Raises:
            Exception: error

        Returns:
            Optional[User]: Instance of User or None
        """
        with DBSession() as session:
            user_cookie_encoded = token
            # return early if cookie not found in request
            if user_cookie_encoded is None:
                return None
            # try to decode the cookie
            try:
                user_cookie_decoded = jwt.decode(
                    user_cookie_encoded,
                    config.SECRET_KEY,
                    algorithms=["HS256"],  # noqa: E501
                )
            except jwt.DecodeError as e:
                # return none if failed to decode cookie
                logger.error(f"Unable to decode cookie due to: {e}")
                return None
            except Exception as e:
                logger.error(f"Unable to decode cookie due to: {e}")
                raise e

            # Fetch and return user if present or None
            stmt = select(ProtagonistDB).where(
                ProtagonistDB.email == user_cookie_decoded["email"]
            )
            user_list: List[ProtagonistDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            # return early if user not found
            if len(user_list) == 0:
                return None
            else:
                return User(user_id=user_list[0].id, **user_list[0].to_dict())

    def authorize_user(
        self: "BaseAuther", user: User, request: Request
    ) -> bool:  # noqa: E501
        """Authorize user actions on resources.

        Args:
            user (User): Instance of User
            request (Request): Instance of Flask Request

        Returns:
            bool: Authorization decision
        """
        return True
