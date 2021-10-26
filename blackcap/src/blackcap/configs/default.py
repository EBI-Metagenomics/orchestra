"""Default blackcap config."""

from blackcap.configs.base import BaseConfig


class DefaultConfig(BaseConfig):
    """Default blackcap config."""

    def get_config_name(self: "DefaultConfig") -> str:
        """Return Config name.

        Returns:
            str: Name of the config
        """
        return "DEFAULT"

    def get_sql_db_uri(self: "DefaultConfig") -> str:
        """Get uri of the sql database.

        Returns:
            str: uri of the sql database
        """
        return f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}/{self.DB_PATH}"  # noqa: E501

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
