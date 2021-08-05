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

    # it's going ot be more performance to keep a counter
    # on this table than queries the schedules count each time
    # we can create a db trigger to keep this updated
    schedules_count = Column(Integer, nullable=False, default=0)
