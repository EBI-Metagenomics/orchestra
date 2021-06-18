"""Base job schema."""

from enum import Enum, unique

from pydantic import BaseModel


class BaseJob(BaseModel):
    """Base job schema."""

    script: str


@unique
class JobStatus(Enum):
    """JobStatus enum."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    CONFIGURING = "CONFIGURING"
    COMPLETING = "COMPLETING"
    RESIZING = "RESIZING"
    SUSPENDED = "SUSPENDED"
