"""Schedule schema."""

from pydantic import BaseModel


class Schedule(BaseModel):
    """Schedule schema."""

    job_id: str
    assigned_cluster_id: str
    status: str = "PENDING"
