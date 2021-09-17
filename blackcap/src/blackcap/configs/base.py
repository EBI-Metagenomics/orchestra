"""Base config class, enum and helper function."""

from abc import ABC, abstractmethod
from typing import Optional

from pydantic.env_settings import BaseSettings

from xdg import xdg_config_home


class BaseConfig(ABC, BaseSettings):
    """Base config class."""

    HOME: str
    FLASK_APP: str = "conductor"
    FLASK_HOST: str = "localhost"
    FLASK_PORT: int = 9991
    FLASK_ENV: str = "development"
    DB_TYPE: str = "postgresql"
    DB_NAME: str = "conductor"
    DB_URI: str = None
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str = "ADD_A_RANDOM_KEY_HERE"  # noqa: S105
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    USER_ACCESS_TOKEN: Optional[str]
    AUTHER: str = "COOKIE"
    MESSENGER: str = "GCP"
    SCHEDULER: str = "RANDOM"
    OBSERVER: str = "ELASTIC"
    GOOGLE_APPLICATION_CREDENTIALS: str = "./keys.json"
    GCP_PROJECT_ID: str = "YOUR_GCP_PROJECT_ID"
    GCP_PUBSUB_TOPIC: str = "test-topic"
    GCP_PUBSUB_SUB_ID: str = "test-sub"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    @abstractmethod
    def get_config_name(self: "BaseConfig") -> str:
        """Return Config name.

        Returns:
            str: Name of the config
        """
        pass

    @abstractmethod
    def get_sql_db_uri(self: "BaseConfig") -> str:
        """Get uri of the sql database.

        Returns:
            str: uri of the sql database
        """
        pass

    class Config:
        """Config for the BaseConfig class."""

        env_file = xdg_config_home() / ("orchestra") / ("conductor.env")


class ConfigOfConfig(BaseSettings):
    "Config for loading config"

    BLACKCAP_CONFIG: str = "DEFAULT"

    class Config:
        """Config for ConfigofConfig class."""

        env_file = xdg_config_home() / ("orchestra") / ("conductor.env")
