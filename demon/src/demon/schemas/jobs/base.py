"""Base job schema."""

from enum import Enum, unique

from demon.schemas.meta.mixins import DBModel, SurrogatePK, TimestampMixin

from pydantic import BaseModel, validator

from sqlalchemy import Column, String


@unique
class JobStatus(Enum):
    """JobStatus enum."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    CONFIGURING = "CONFIGURING"
    COMPLETING = "COMPLETING"
    RESIZING = "RESIZING"
    SUSPENDED = "SUSPENDED"


class BaseJob(BaseModel):
    """Base job schema."""

    script: str
    status: JobStatus = JobStatus.PENDING

    @validator("status", always=True)
    def convert_status_enum_to_str(cls: "BaseJob", v: JobStatus) -> str:
        """Convert enum to string.

        Args:
            v (JobStatus): JobStatus enum

        Returns:
            str: Str repr of enum
        """
        return v.value


class BaseJobDB(DBModel, TimestampMixin, SurrogatePK):
    """Base job table for DB."""

    __tablename__ = "job"
    name = Column(String(), nullable=False)
    script = Column(String(), nullable=False)
    status = Column(String(), nullable=False, default="PENDING")
