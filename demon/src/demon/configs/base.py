"""Base config class, enum and helper function."""

from abc import ABC, abstractmethod

from pydantic import BaseSettings

from xdg import xdg_config_home


class BaseConfig(ABC, BaseSettings):
    """Base config class."""

    HOME: str
    DB_TYPE: str = "postgresql"
    DB_NAME: str = "demon"
    DB_URI: str = None
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MESSENGER = "GCP"
    CLUSTER = "SLURM"
    GOOGLE_APPLICATION_CREDENTIALS = "./keys.json"
    GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID"
    GCP_PUBSUB_TOPIC = "test-topic"
    GCP_PUBSUB_SUB_ID = "test-sub"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    @abstractmethod
    def get_sql_db_uri() -> str:
        """Get uri of the sql database.

        Returns:
            str: uri of the sql database
        """
        pass

    class Config:
        """Config for the BaseConfig class."""

        env_file = xdg_config_home() / ("orchestra") / ("demon.env")
