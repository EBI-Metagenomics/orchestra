"""Base config class, enum and helper function."""

from abc import ABC, abstractmethod


class BaseConfig(ABC):
    """Base config class."""

    @abstractmethod
    def get_sql_db_uri() -> str:
        """Get uri of the sql database.

        Returns:
            str: uri of the sql database
        """
        pass
