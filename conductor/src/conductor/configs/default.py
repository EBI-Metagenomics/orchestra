"""Default conductor config."""

from conductor.configs.base import BaseConfig

from pydantic import BaseSettings

from xdg import xdg_config_home


class DefaultConfig(BaseConfig, BaseSettings):
    """Default conductor config."""

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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "ADD_A_RANDOM_KEY_HERE"  # noqa: S105
    MESSENGER = "GCP"
    GOOGLE_APPLICATION_CREDENTIALS = "./keys.json"
    GCP_PROJECT_ID = "YOUR_GCP_PROJECT_ID"
    GCP_PUBSUB_TOPIC = "test-topic"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    def get_sql_db_uri(self: "DefaultConfig") -> str:
        """Get uri of the sql database.

        Returns:
            str: uri of the sql database
        """
        return f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa: E501

    @property
    def SQLALCHEMY_DATABASE_URI(self: "DefaultConfig") -> str:
        """Get db uri for sqlalchemy.

        Returns:
            str: Database uri for sqlalchemy
        """
        if self.DB_URI is not None:
            return self.DB_URI
        else:
            return self.get_sql_db_uri()

    class Config:
        """Config for the BaseConfig class."""

        env_file = xdg_config_home() / ("orchestra") / ("conductor.env")
