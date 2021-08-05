"""Schedule BLoCs."""

from datetime import datetime
from typing import List

from conductor import DBSession, global_config
from conductor.extentions import messenger, scheduler
from conductor.models.schedule import ScheduleDB
from conductor.schemas.api.schedule.delete import ScheduleDelete
from conductor.schemas.api.schedule.get import (
    ScheduleGetQueryParams,
    ScheduleQueryType,
)  # noqa: E501
from conductor.schemas.api.schedule.post import ScheduleCreate
from conductor.schemas.api.schedule.put import ScheduleUpdate
from conductor.schemas.message import Message, MessageType

from logzero import logger

from sqlalchemy import select


def create_schedule(
    schedule_create_list: List[ScheduleCreate],
) -> List[ScheduleDB]:  # noqa: E501
    """Create schedules and save to DB from ScheduleCreate requests.

    Args:
        schedule_create_list (List[ScheduleCreate]): List of ScheduleCreate request  # noqa: E501

    Returns:
        List[ScheduleDB]: Instance of Schedule from DB
    """
    try:

        schedule_list: List[ScheduleDB] = [
            scheduler.schedule(schedule_create)
            for schedule_create in schedule_create_list
        ]

        # publish msg to demon
        for schedule in schedule_list:
            message = Message(
                msg_type=MessageType.TO_DEMON_SCHEDULE_MSG,
                data=schedule.dict(),
                timestamp=str(datetime.now()),
            )
            messenger.publish(message, global_config.GCP_PUBSUB_TOPIC)
        return schedule_list
    except Exception as e:
        logger.error(f"Unable to create and publish schedules: {e}")


def get_schedules(query_params: ScheduleGetQueryParams) -> List[ScheduleDB]:
    """Query DB for schedules.

    Args:
        query_params (ScheduleGetQueryParams): Query params from request

    Returns:
        List[Schedule]: List of schedules returned from DB
    """
    schedule_list: List[ScheduleDB]
    if query_params.query_type == ScheduleQueryType.GET_ALL_SCHEDULES:
        stmt = select(ScheduleDB)
        with DBSession() as session:
            try:
                schedule_list: List[ScheduleDB] = (
                    session.execute(stmt).scalars().all()
                )  # noqa: E501
                return schedule_list
            except Exception as e:
                session.rollback()
                logger.error(f"Unable to fetch schedules due to {e}")
    if query_params.query_type == ScheduleQueryType.GET_SCHEDULE_BY_ID:
        stmt = select(ScheduleDB).where(
            ScheduleDB.id == query_params.schedule_id
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
    if (
        query_params.query_type
        == ScheduleQueryType.GET_SCHEDULES_BY_PROTAGONIST_ID  # noqa: E501
    ):
        stmt = select(ScheduleDB).where(
            ScheduleDB.protagonist_id == query_params.protagonist_id
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
    return schedule_list


def update_schedule(schedule_update: ScheduleUpdate) -> ScheduleDB:
    """Update schedule in the DB from ScheduleUpdate request.

    Args:
        schedule_update (ScheduleUpdate): ScheduleUpdate request

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
            if len(schedule_list) == 1:
                schedule_update_dict = schedule_update.dict()
                schedule_update_dict.pop("schedule_id")
                updated_schedule = schedule_list[0].update(
                    session, **schedule_update.dict()
                )  # noqa: E501
                return updated_schedule
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to update schedule: {schedule_update.dict()} due to {e}"  # noqa: E501
            )
            # TODO: Raise error


def delete_schedule(schedule_delete: ScheduleDelete) -> ScheduleDB:
    """Delete schedule in the DB from ScheduleDelete request.

    Args:
        schedule_delete (ScheduleDelete): ScheduleDelete request

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
            if len(schedule_list) == 1:
                deleted_schedule = schedule_list[0].delete(session)
                return deleted_schedule
        except Exception as e:
            session.rollback()
            logger.error(
                f"Unable to delete schedule: {schedule_delete.dict()} due to {e}"  # noqa: E501
            )
            # TODO: Raise error