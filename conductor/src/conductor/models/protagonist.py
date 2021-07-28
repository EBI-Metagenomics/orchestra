"""Protagonist DBModel."""


from conductor.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)  # noqa: E501

from sqlalchemy import Boolean, Column, LargeBinary, String


class ProtagonistDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Protagonist table."""

    __tablename__ = "protagonist"
    name = Column(String(), nullable=False)
    organisation = Column(String(), nullable=True)
    email = Column(String(), unique=True, nullable=False)
    # Hash password before storing it here
    password = Column(LargeBinary(128), nullable=True)
    active = Column(Boolean(), default=False)
