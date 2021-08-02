"""Schedule DBModel."""


from conductor.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)  # noqa: E501
from conductor.models.meta.orm import reference_col

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship


class ScheduleDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Schedule table."""

    __tablename__ = "schedule"
    job_id = reference_col("job")
    job = relationship("JobDB", backref="schedules")
    assigned_cluster_id = reference_col("cluster")
    assigned_cluster = relationship("ClusterDB", backref="schedules")
    status = Column(String(), nullable=False, default="PENDING")
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    protagonist_id = reference_col("protagonist")
    protagonist = relationship("ProtagonistDB", backref="schedules")
