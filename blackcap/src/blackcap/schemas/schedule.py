"""Schedule schema."""

from typing import Optional

from blackcap.schemas.job import Job

from pydantic import BaseModel
from pydantic.types import UUID4


class Schedule(BaseModel):
    """Schedule schema."""

    schedule_id: Optional[UUID4]
    user_id: Optional[UUID4]
    job_id: UUID4
    job: Optional[Job]
    assigned_cluster_id: Optional[UUID4]
    messenger: Optional[str]
    messenger_queue: Optional[str]
    status: str = "PENDING"
