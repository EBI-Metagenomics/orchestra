"""Mixins for database models."""

import uuid
from datetime import datetime
from typing import Any, List, Optional, Union

from conductor.extentions import DBSession
from conductor.models.meta.helpers import GUID

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base


# declarative base class
Base = declarative_base()


class TimestampMixin(object):
    """Mixin that adds timestamp."""

    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD operations."""

    @classmethod
    def create(cls: Any, **kwargs: Any) -> Any:
        """Create a new record and save it to the database.

        Args:
            **kwargs (Any): kwargs to pass to cls for init

        Returns:
            Any: Instance of self
        """
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def bulk_create(cls: Any, list: List[Any]) -> Any:
        """Create a new records and save them to the database.

        Args:
            list (List[Any]): List of self

        Returns:
            Any: True if scuccess
        """
        instance_list: List[Any] = []
        for item in list:
            instance_list.append(cls(**item))
        with DBSession() as session:
            session.bulk_save_objects(instance_list)
            session.commit()
        return True

    def update(self: "CRUDMixin", commit: bool = True, **kwargs: Any) -> Any:
        """Update specific fields of a record.

        Args:
            commit (bool): Flag to control commit behaviour. Defaults to True.
            **kwargs (Any): kwargs to update cls params

        Returns:
            Any: Instance of self
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    @classmethod
    def bulk_update(cls: Any, list: List[Any]) -> Any:
        """Create a new records and save them to the database.

        Args:
            list (List[Any]): List of instances of self

        Returns:
            Any: List of updated instances self
        """
        instance_list: List[Any] = []
        for item in list:
            instance_list.append(cls(**item))
        with DBSession() as session:
            session.bulk_update_mappings(list)
            session.commit()
        return instance_list

    def save(self: "CRUDMixin", commit: bool = True) -> Any:
        """Save the record.

        Args:
            commit (bool): Flag to control commit behaviour. Defaults to True. # noqa: E501

        Returns:
            Any: Instance of self
        """
        with DBSession() as session:
            session.add(self)
            if commit:
                session.commit()
        return self

    def delete(self: "CRUDMixin", commit: bool = True) -> Union[bool, Any]:
        """Remove the record from the database.

        Args:
            commit (bool): Flag to control commit behaviour. Defaults to True. # noqa: E501

        Returns:
            Union[bool, Any]: True if commit is successful
        """
        with DBSession() as session:
            session.delete(self)
            return commit and session.commit()


class DBModel(CRUDMixin, Base):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """Adds a surrogate int 'primary key' column named ``id`` to any orm class."""  # noqa: E501

    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls: Any, record_id: Union[str, int]) -> Union[None, Any]:
        """Get record by ID.

        Args:
            record_id (Union[str, int]): Id of the record to fetch

        Returns:
            Union[None, Any]: Return the instance of self if found or else None
        """
        if any(
            (
                isinstance(record_id, str) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


class SurrogatePKUUID(object):
    """Adds a surrogate int 'primary key' column named ``id`` to any orm class."""  # noqa: E501

    __table_args__ = {"extend_existing": True}

    id = Column(GUID, primary_key=True, default=lambda: str(uuid.uuid4()))

    @classmethod
    def get_by_uuid(
        cls: Any, record_id: Union[str, uuid.UUID]
    ) -> Optional[Any]:  # noqa: E501
        """Get record by ID.

        Args:
            record_id (Union[str, uuid.UUID]): Id of the record to fetch

        Returns:
            Union[None, Any]: Return the instance of self if found or else None
        """
        if any(
            (
                isinstance(record_id, str),
                isinstance(record_id, uuid.UUID),
            )
        ):
            return cls.query.get(uuid.UUID(str(record_id)))
        return None
