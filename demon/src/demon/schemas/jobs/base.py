"""Base job schema."""

from enum import Enum, unique

from demon.schemas.meta.mixins import DBModel, SurrogatePK, TimestampMixin

from pydantic import BaseModel

from sqlalchemy import Column, String


class BaseJob(BaseModel):
    """Base job schema."""

    script: str


class BaseJobDB(DBModel, TimestampMixin, SurrogatePK):
    """Base job table for DB."""

    __tablename___ = "job"
    script = Column(String(), nullable=False)


@unique
class JobStatus(Enum):
    """JobStatus enum."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    CONFIGURING = "CONFIGURING"
    COMPLETING = "COMPLETING"
    RESIZING = "RESIZING"
    SUSPENDED = "SUSPENDED"
