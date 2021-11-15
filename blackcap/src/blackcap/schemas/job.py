"""Job schema."""

from typing import Dict, Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class Job(BaseModel):
    """Job schema."""

    job_id: Optional[UUID4]
    name: str
    description: Optional[str]
    job_type: str = ""
    specification: Dict = {}
    job_metadata: Dict = {}
    script: Optional[str]
