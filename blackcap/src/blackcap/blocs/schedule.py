"""Schedule BLoCs."""

from datetime import datetime
from typing import List

from blackcap.configs import config_registry
from blackcap.db import DBSession
from blackcap.scheduler import scheduler_registry
from blackcap.models.schedule import ScheduleDB
from blackcap.schemas.api.schedule.delete import ScheduleDelete
from blackcap.schemas.api.schedule.get import (
    ScheduleGetQueryParams,
    ScheduleQueryType,
)  # noqa: E501
from blackcap.schemas.api.schedule.post import ScheduleCreate
from blackcap.schemas.api.schedule.put import ScheduleUpdate
from blackcap.schemas.message import Message, MessageType
from blackcap.schemas.schedule import Schedule
from blackcap.tasks.pub_messenger import publish_messenger

from logzero import logger

from sqlalchemy import select


config = config_registry.get_config()
scheduler = scheduler_registry.get_scheduler(config.SCHEDULER)


##################
# CRUD
##################


def create_schedule(
    schedule_create_list: List[ScheduleCreate],
) -> List[Schedule]:  # noqa: E501
    """Create schedules and save to DB from ScheduleCreate requests.

    Args:
        schedule_create_list (List[ScheduleCreate]): List of ScheduleCreate request  # noqa: E501

    Returns:
        List[Schedule]: Instance of Schedule from DB
    """
    schedule_list: List[Schedule] = [
        scheduler.schedule(schedule_create)
        for schedule_create in schedule_create_list  # noqa: E501
    ]

    # publish msg to demon
    for schedule in schedule_list:
        message = Message(
            msg_type=MessageType.TO_DEMON_SCHEDULE_MSG,
            data=schedule.dict(),
            timestamp=str(datetime.now()),
        )
        publish_messenger.delay(message.dict(), schedule.messenger_queue)

    return schedule_list


def get_schedules(query_params: ScheduleGetQueryParams) -> List[ScheduleDB]:
    """Query DB for schedules.

    Args:
        query_params (ScheduleGetQueryParams): Query params from request

    Raises:
        Exception: error

    Returns:
        List[Schedule]: List of schedules returned from DB
    """
    schedule_list: List[ScheduleDB]
    if query_params.query_type == ScheduleQueryType.GET_ALL_SCHEDULES:
        stmt = select(ScheduleDB)
    if query_params.query_type == ScheduleQueryType.GET_SCHEDULE_BY_ID:
        stmt = select(ScheduleDB).where(
            ScheduleDB.id == query_params.schedule_id
        )  # noqa: E501
    if (
        query_params.query_type
        == ScheduleQueryType.GET_SCHEDULES_BY_PROTAGONIST_ID  # noqa: E501
    ):
        stmt = select(ScheduleDB).where(
            ScheduleDB.protagonist_id == query_params.protagonist_id
        )  # noqa: E501
    if (
        query_params.query_type
        == ScheduleQueryType.GET_SCHEDULES_BY_CLUSTER_ID  # noqa: E501
    ):
        stmt = select(ScheduleDB).where(
            ScheduleDB.assigned_cluster_id == query_params.cluster_id
        )  # noqa: E501

    with DBSession() as session:
        try:
            schedule_list: List[ScheduleDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            return schedule_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch schedules due to {e}")
            raise e

    return schedule_list


def update_schedule(schedule_update: ScheduleUpdate) -> ScheduleDB:
    """Update schedule in the DB from ScheduleUpdate request.

    Args:
        schedule_update (ScheduleUpdate): ScheduleUpdate request

    Raises:
        Exception: error

    Returns:
        ScheduleDB: Instance of Updated Schedule
    """
    stmt = select(ScheduleDB).where(
        ScheduleDB.id == schedule_update.schedule_id
    )  # noqa: E501
    with DBSession() as session:
        try:
            schedule_list: List[ScheduleDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            # if schedule_list is None:
            # raise NotFound exception - 404
            if len(schedule_list) == 1:
                schedule_update_dict = schedule_update.dict(exclude_defaults=True)
                schedule_update_dict.pop("schedule_id")
                updated_schedule = schedule_list[0].update(
                    session, **schedule_update_dict
                )  # noqa: E501
                return updated_schedule
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to update schedule: {schedule_update.dict()} due to {e}"  # noqa: E501
            )
            raise e


def delete_schedule(schedule_delete: ScheduleDelete) -> ScheduleDB:
    """Delete schedule in the DB from ScheduleDelete request.

    Args:
        schedule_delete (ScheduleDelete): ScheduleDelete request

    Raises:
        Exception: error

    Returns:
        ScheduleDB: Instance of Deleted Schedule
    """
    stmt = select(ScheduleDB).where(
        ScheduleDB.id == schedule_delete.schedule_id
    )  # noqa: E501
    with DBSession() as session:
        try:
            schedule_list: List[ScheduleDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            if not schedule_list:
                # TODO: raise not found exception
                pass
            if len(schedule_list) == 1:
                deleted_schedule = schedule_list[0].delete(session)
                return deleted_schedule
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to delete schedule: {schedule_delete.dict()} due to {e}"  # noqa: E501
            )
            raise e


##################
# Flows
##################
