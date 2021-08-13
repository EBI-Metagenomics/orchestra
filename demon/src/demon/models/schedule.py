"""Schedule DBModel."""


from demon.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)  # noqa: E501
from demon.models.meta.orm import reference_col

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship


class ScheduleDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Schedule table."""

    __tablename__ = "schedule"
    job_id = reference_col("job")
    job = relationship("JobDB", backref="schedules")
    # TODO: this should be an enum
    status = Column(String, nullable=False, default="PENDING")
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    protagonist_id = Column(String(), nullable=False)
