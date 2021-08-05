"""Cluster DBModel."""


from conductor.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)  # noqa: E501


from sqlalchemy import Column, String


class ClusterDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Cluster table."""

    __tablename__ = "cluster"
    name = Column(String(), nullable=False)
    cluster_type = Column(String(), nullable=False)
    status = Column(String(), nullable=False)
    cluster_caps = Column(String(), nullable=True)
    messenger = Column(String(), nullable=False, default="GCP")
    messenger_queue = Column(String(), nullable=False)
