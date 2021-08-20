"""Schedule schema."""

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class Schedule(BaseModel):
    """Schedule schema."""

    schedule_id: Optional[UUID4]
    user_id: Optional[UUID4]
    job_id: UUID4
    assigned_cluster_id: Optional[UUID4]
    messenger: Optional[str]
    messenger_queue: Optional[str]
    status: str = "PENDING"
