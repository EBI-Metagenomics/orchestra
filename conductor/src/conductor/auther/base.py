"""Base Auther class."""

from abc import ABC, abstractclassmethod
from typing import List

from conductor.models.protagonist import ProtagonistDB
from conductor.schemas.api.user.post import UserCreate


class BaseAuther(ABC):
    """Base Auther class."""

    @abstractclassmethod
    def register_user(
        self: "BaseAuther", user_create_list: List[UserCreate]
    ) -> List[ProtagonistDB]:  # noqa: E501
        """Register user."""
        pass

    @abstractclassmethod
    def login_user(
        self: "BaseAuther",
    ) -> None:
        """Login user."""
        pass

    @abstractclassmethod
    def logout_user(
        self: "BaseAuther",
    ) -> None:
        """Logout user."""
        pass

    @abstractclassmethod
    def authorize_user(
        self: "BaseAuther",
    ) -> None:
        """Authorize user."""
        pass
