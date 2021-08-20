"""Job schema."""

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class Job(BaseModel):
    """Job schema."""

    job_id: Optional[UUID4]
    name: str
    script: str
