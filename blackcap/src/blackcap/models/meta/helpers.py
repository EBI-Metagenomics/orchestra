"""SQL helpers."""

import uuid
from typing import Any

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import CHAR, TypeDecorator


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    Credit: https://gist.github.com/gmolveau/7caeeefe637679005a7bb9ae1b5e421e
    TODO: Change Any to more concrete types
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self: "GUID", dialect: Any) -> Any:
        """Return column type to create based on dialect.

        Args:
            dialect (Any): sql dialect

        Returns:
            Any: column type to create
        """
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self: "GUID", value: Any, dialect: Any) -> Any:
        """Receive a bound parameter value to be converted.

        Args:
            value (Any): [description]
            dialect (Any): [description]

        Returns:
            Any: [description]
        """
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self: "GUID", value: Any, dialect: Any) -> Any:
        """Receive a result-row column value to be converted.

        Args:
            value (Any): [description]
            dialect (Any): [description]

        Returns:
            Any: [description]
        """
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
