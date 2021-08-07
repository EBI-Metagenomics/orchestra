"""Job DBModel."""


from demon.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)  # noqa: E501

from sqlalchemy import Column, Integer, String


class JobDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Job table."""

    __tablename__ = "job"
    name = Column(String(), nullable=False)
    script = Column(String(), nullable=False)
    cluster_caps_req = Column(String(), nullable=True)
    protagonist_id = Column(String(), nullable=False)

    # it's going to be more performant to keep a counter
    # on this table than to query the schedules table
    schedules_count = Column(Integer, nullable=False, default=0)
