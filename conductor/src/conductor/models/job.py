"""Job DBModel."""


from conductor.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)  # noqa: E501
from conductor.models.meta.orm import reference_col

from sqlalchemy import Column, Integer, String

# from sqlalchemy.orm import relationship


class JobDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Job table."""

    __tablename__ = "job"
    serialize_rules = ("-protagonist.jobs",)
    name = Column(String(), nullable=False)
    script = Column(String(), nullable=False)

    cluster_caps_req = Column(String(), nullable=True)

    protagonist_id = reference_col("protagonist")
    # protagonist = relationship("ProtagonistDB", backref="jobs")

    # it's going ot be more performance to keep a counter
    # on this table than queries the schedules count each time
    # we can create a db trigger to keep this updated
    # TODO: add a signal to keep this value updated
    schedules_count = Column(Integer, nullable=False, default=0)
