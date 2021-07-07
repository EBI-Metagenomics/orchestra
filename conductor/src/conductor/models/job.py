"""Job DBModel."""


from conductor.models.meta.helpers import GUID
from conductor.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)  # noqa: E501

# from conductor.models.meta.orm import reference_col

from sqlalchemy import Column, DateTime, String

# from sqlalchemy.orm import relationship


class JobDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Job table."""

    __tablename__ = "job"
    name = Column(String(), nullable=False)
    script = Column(String(), nullable=False)
    status = Column(String(), nullable=False)
    assigned_cluster_id = Column(GUID(), nullable=False)
    cluster_caps_req = Column(String(), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    # protagonist_id = reference_col("protagonist")
    # protagonist = relationship()
