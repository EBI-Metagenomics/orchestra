"""Schedule schema."""

from typing import Optional

from pydantic import BaseModel


class Schedule(BaseModel):
    """Schedule schema."""

    user_id: Optional[str]
    job_id: str
    assigned_cluster_id: Optional[str]
    status: str = "PENDING"
