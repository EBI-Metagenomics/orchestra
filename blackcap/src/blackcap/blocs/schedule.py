"""Schedule BLoCs."""

from typing import List


from logzero import logger
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy import select

from blackcap.configs import config_registry
from blackcap.db import DBSession
from blackcap.models.schedule import ScheduleDB
from blackcap.scheduler import scheduler_registry
from blackcap.schemas.api.schedule.delete import ScheduleDelete
from blackcap.schemas.api.schedule.get import (
    ScheduleGetQueryParams,
    ScheduleQueryType,
)
from blackcap.schemas.api.schedule.post import ScheduleCreate
from blackcap.schemas.api.schedule.put import ScheduleUpdate
from blackcap.schemas.schedule import Schedule
from blackcap.schemas.user import User

config = config_registry.get_config()
scheduler = scheduler_registry.get_scheduler(config.SCHEDULER)


##################
# CRUD
##################


def create_schedule(
    schedule_create_list: List[ScheduleCreate], user_creds: User
) -> List[Schedule]:
    """Create schedules and save to DB from ScheduleCreate requests.

    Args:
        schedule_create_list (List[ScheduleCreate]): List of ScheduleCreate request
        user_creds (User): User credentials.

    Raises:
        Exception: database error

    Returns:
        List[Schedule]: Instance of Schedule from DB
    """
    with DBSession() as session:
        try:
            schedule_db_create_list: List[ScheduleDB] = [
                ScheduleDB(
                    protagonist_id=user_creds.user_id,
                    **schedule.dict(),
                )
                for schedule in schedule_create_list
            ]
            ScheduleDB.bulk_create(schedule_db_create_list, session)
            return [
                Schedule(schedule_id=obj.id, **obj.to_dict())
                for obj in schedule_db_create_list
            ]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to create schedules: {e}")
            raise e


def get_schedules(
    query_params: ScheduleGetQueryParams, user_creds: User
) -> List[Schedule]:
    """Query DB for schedules.

    Args:
        query_params (ScheduleGetQueryParams): Query params from request
        user_creds (User): User credentials.

    Raises:
        e: error
        Exception: error

    Returns:
        List[Schedule]: List of schedules returned from DB
    """
    schedule_list: List[ScheduleDB]
    if query_params.query_type == ScheduleQueryType.GET_ALL_SCHEDULES:
        stmt = select(ScheduleDB).where(ScheduleDB.protagonist_id == user_creds.user_id)
    if query_params.query_type == ScheduleQueryType.GET_SCHEDULE_BY_ID:
        if query_params.schedule_id is None:
            e = ValidationError(
                errors=[
                    ErrorWrapper(ValueError("field required"), "schedule_id"),
                ],
                model=ScheduleGetQueryParams,
            )
            raise e
        stmt = select(ScheduleDB).where(ScheduleDB.id == query_params.schedule_id)
    if query_params.query_type == ScheduleQueryType.GET_SCHEDULES_BY_PROTAGONIST_ID:
        if query_params.protagonist_id is None:
            e = ValidationError(
                errors=[
                    ErrorWrapper(ValueError("field required"), "protagonist_id"),
                ],
                model=ScheduleGetQueryParams,
            )
            raise e
        stmt = (
            select(ScheduleDB)
            .where(ScheduleDB.protagonist_id == user_creds.user_id)
            .where(ScheduleDB.protagonist_id == query_params.protagonist_id)
        )
    if query_params.query_type == ScheduleQueryType.GET_SCHEDULES_BY_CLUSTER_ID:
        if query_params.cluster_id is None:
            e = ValidationError(
                errors=[
                    ErrorWrapper(ValueError("field required"), "protagonist_id"),
                ],
                model=ScheduleGetQueryParams,
            )
            raise e
        stmt = (
            select(ScheduleDB)
            .where(ScheduleDB.protagonist_id == user_creds.user_id)
            .where(ScheduleDB.assigned_cluster_id == query_params.cluster_id)
        )

    with DBSession() as session:
        try:
            schedule_db_list: List[ScheduleDB] = session.execute(stmt).scalars().all()
            schedule_list: List[Schedule] = [
                Schedule(schedule_id=obj.id, **obj.to_dict())
                for obj in schedule_db_list
            ]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch schedules due to {e}")
            raise e
    return schedule_list


def update_schedule(
    schedule_update_list: List[ScheduleUpdate], user_creds: User
) -> List[Schedule]:
    """Update schedule in the DB from ScheduleUpdate request.

    Args:
        schedule_update_list (List[ScheduleUpdate]): ScheduleUpdate request
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        List[ScheduleDB]: List of Instance of Updated Schedule
    """
    stmt = (
        select(ScheduleDB)
        .where(ScheduleDB.protagonist_id == user_creds.user_id)
        .where(
            ScheduleDB.id.in_(
                [
                    schedule_update.schedule_id
                    for schedule_update in schedule_update_list
                ]
            )
        )
    )
    with DBSession() as session:
        try:
            schedule_db_update_list: List[ScheduleDB] = (
                session.execute(stmt).scalars().all()
            )
            updated_schedule_list = []
            for schedule in schedule_db_update_list:
                for schedule_update in schedule_update_list:
                    if schedule_update.schedule_id == schedule.id:
                        schedule_update_dict = schedule_update.dict(
                            exclude_defaults=True
                        )
                        schedule_update_dict.pop("schedule_id")
                        updated_schedule = schedule.update(
                            session, **schedule_update_dict
                        )
                        updated_schedule_list.append(
                            Schedule(
                                schedule_id=updated_schedule.id,
                                **updated_schedule.to_dict(),
                            )
                        )
            return updated_schedule_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to update schedule: {schedule.to_dict()} due to {e}")
            raise e


def delete_schedule(
    schedule_delete_list: List[ScheduleDelete], user_creds: User
) -> List[ScheduleDB]:
    """Delete schedule in the DB from ScheduleDelete request.

    Args:
        schedule_delete_list (List[ScheduleDelete]): List of ScheduleDelete request
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        ScheduleDB: Instance of Deleted Schedule
    """
    stmt = (
        select(ScheduleDB)
        .where(ScheduleDB.protagonist_id == user_creds.user_id)
        .where(
            ScheduleDB.id.in_(
                [schedule.schedule_id for schedule in schedule_delete_list]
            )
        )
    )
    with DBSession() as session:
        try:
            schedule_db_delete_list: List[ScheduleDB] = (
                session.execute(stmt).scalars().all()
            )
            deleted_schedule_list = []
            for schedule in schedule_db_delete_list:
                schedule.delete(session)
                deleted_schedule_list.append(
                    Schedule(schedule_id=schedule.id, **schedule.to_dict())
                )
            return deleted_schedule_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to delete schedule: {schedule.to_dict()} due to {e}")
            raise e


##################
# Flows
##################
