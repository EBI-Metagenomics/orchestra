"""Base Auther class."""

from abc import ABC, abstractclassmethod
from typing import List, Optional, Tuple

from conductor.models.protagonist import ProtagonistDB
from conductor.schemas.api.auth.post import AuthUserCreds
from conductor.schemas.api.user.post import UserCreate
from conductor.schemas.user import User

from flask import Request


class BaseAuther(ABC):
    """Base Auther class."""

    @abstractclassmethod
    def register_user(
        self: "BaseAuther", user_create_list: List[UserCreate]
    ) -> List[ProtagonistDB]:  # noqa: E501
        """Register user.

        Args:
            user_create_list (List[UserCreate]): List of users to register

        Raises:
            Exception: error  # noqa: DAR402

        Returns:
            List(ProtagonistDB): List of registered users  # noqa: DAR202
        """
        pass

    @abstractclassmethod
    def login_user(
        self: "BaseAuther", user_creds: AuthUserCreds
    ) -> Optional[Tuple[ProtagonistDB, str]]:
        """Login user.

        Args:
            user_creds (AuthUserCreds): user creds

        Raises:
            Exception: error  # noqa: DAR402

        Returns:
            Optional[Tuple[ProtagonistDB, str]]: user and cookie tuple or None
        """
        pass

    @abstractclassmethod
    def logout_user(
        self: "BaseAuther",
    ) -> None:
        """Logout user."""
        pass

    @abstractclassmethod
    def extract_user_from_flask_req(
        self: "BaseAuther", request: Request
    ) -> Optional[ProtagonistDB]:  # noqa: E501
        """Extract user from flask request.

        Args:
            request (Request): Instance of flask request

        Raises:
            Exception: error  # noqa: DAR402

        Returns:
            Optional[ProtagonistDB]: Instance of ProtagonistDB or None
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
