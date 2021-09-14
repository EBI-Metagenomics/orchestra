"""Base Auther class."""

from abc import ABC, abstractclassmethod
from typing import List, Optional, Tuple

from blackcap.schemas.api.auth.post import AuthUserCreds
from blackcap.schemas.api.user.post import UserCreate
from blackcap.schemas.user import User

from flask import Request


class BaseAuther(ABC):
    """Base Auther class."""

    CONFIG_KEY = "AUTHER"
    CONFIG_KEY_DEF_VAL = "COOKIE"

    # Change this value in custom auther implementations.
    CONFIG_KEY_VAL = "COOKIE"

    @abstractclassmethod
    def register_user(
        self: "BaseAuther", user_create_list: List[UserCreate]
    ) -> List[User]:  # noqa: E501
        """Register user.

        Args:
            user_create_list (List[UserCreate]): List of users to register

        Raises:
            Exception: error  # noqa: DAR402

        Returns:
            List(User): List of registered users  # noqa: DAR202
        """
        pass

    @abstractclassmethod
    def login_user(
        self: "BaseAuther", user_creds: AuthUserCreds
    ) -> Optional[Tuple[User, str]]:
        """Login user.

        Args:
            user_creds (AuthUserCreds): user creds

        Raises:
            Exception: error  # noqa: DAR402

        Returns:
            Optional[Tuple[User, str]]: user and cookie tuple or None
        """
        pass

    @abstractclassmethod
    def logout_user(
        self: "BaseAuther",
    ) -> None:
        """Logout user."""
        pass

    @abstractclassmethod
    def extract_user_from_token(
        self: "BaseAuther", token: str
    ) -> Optional[User]:  # noqa: E501
        """Extract user from token.

        Args:
            token (str): user access token

        Raises:
            Exception: error  # noqa: DAR402

        Returns:
            Optional[User]: Instance of User or None
        """
        pass

    @abstractclassmethod
    def authorize_user(
        self: "BaseAuther", user: User, request: Request
    ) -> bool:  # noqa: E501
        """Authorize user actions on resources.

        Args:
            user (User): Instance of User
            request (Request): Instance of Flask Request

        Returns:
            bool: Authorization decision  # noqa: DAR202
        """
        pass
