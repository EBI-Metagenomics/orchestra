"""Job schema."""

from pydantic import BaseModel


class Job(BaseModel):
    """Job schema."""

    name: str
    script: str
