"""Schedule BLoCs."""

from typing import List


from logzero import logger
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


from blackcap.configs import config_registry
from blackcap.blocs.job import get_job
from blackcap.db import DBSession
from blackcap.flow import Flow, FlowExecError, FuncProp, get_outer_function, Prop, Step
from blackcap.flow.step import dummy_backward
from blackcap.messenger import messenger_registry
from blackcap.models.schedule import ScheduleDB
from blackcap.scheduler import scheduler_registry
from blackcap.schemas.api.job.get import JobGetQueryParams, JobQueryType
from blackcap.schemas.api.schedule.delete import ScheduleDelete
from blackcap.schemas.api.schedule.get import (
    ScheduleGetQueryParams,
    ScheduleQueryType,
)
from blackcap.schemas.api.schedule.post import ScheduleCreate
from blackcap.schemas.api.schedule.put import ScheduleUpdate
from blackcap.schemas.job import Job
from blackcap.schemas.message import Message, MessageType
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


def get_schedule(
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


def create_schedule_with_scheduler(inputs: List[Prop]) -> List[Prop]:
    """Create schedule db entry step function.

    Args:
        inputs (List[Prop]):
            Expects
                0: schedule_create_request_list
                    Prop(data=schedule_create_request_list, description="List of jobs to schedule") # noqa: B950
                2: user
                    Prop(data=user, description="User")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Created schedule objects

            Prop(data=created_schedule_list, description="List of created schedule Objects") # noqa: B950
    """
    try:
        schedule_create_request_list: List[ScheduleCreate] = inputs[0].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        processed_schedule_create_request_list = [
            scheduler.schedule(schedule_create)
            for schedule_create in schedule_create_request_list
        ]
        created_schedule_list = create_schedule(
            processed_schedule_create_request_list, user
        )
    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Creating DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=created_schedule_list, description="List of created schedule Objects")
    ]


def create_schedule_db_entry(inputs: List[Prop]) -> List[Prop]:
    """Create schedule db entry step function.

    Args:
        inputs (List[Prop]):
            Expects
                0: schedule_create_request_list
                    Prop(data=schedule_create_request_list, description="List of create schedule objects") # noqa: B950
                2: user
                    Prop(data=user, description="User")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Created schedule objects

            Prop(data=created_schedule_list, description="List of created schedule Objects") # noqa: B950
    """
    try:
        schedule_create_request_list: List[ScheduleCreate] = inputs[0].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        created_schedule_list = create_schedule(schedule_create_request_list, user)
    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Creating DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=created_schedule_list, description="List of created schedule Objects")
    ]


def revert_schedule_db_entry(inputs: List[Prop]) -> List[Prop]:
    """Delete db entry step function.

    Args:
        inputs (List[Prop]):
            Expects
                0: schedule_create_request_list
                    Prop(data=schedule_create_request_list, description="List of create schedule objects") # noqa: B950
                1: user
                    Prop(data=user, description="User")
                2: created_schedule_list
                    Prop(data=created_data_list, description="List of created schedule objects") # noqa: B950

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Deleted schedule objects

            Prop(data=deleted_schedule_list, description="List of deleted schedule Objects") # noqa: B950
    """
    try:
        created_schedule_list: List[Schedule] = inputs[2].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        deleted_schedule_list = delete_schedule(created_schedule_list, user)
    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Deleting DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=deleted_schedule_list, description="List of deleted schedule Objects")
    ]


def publish_schedule_message(inputs: List[Prop]) -> List[Prop]:
    """Publish schedule message step function.

    Args:
        inputs (List[Prop]):
            Expects
                0: created_schedule_list
                    Prop(data=created_schedule_list, description="List of created schedule objects") # noqa: B950
                1: user
                    Prop(data=user, description="User")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Created schedule objects

            Prop(data=created_schedule_list, description="List of created schedule Objects") # noqa: B950
    """
    try:
        created_schedule_list: List[ScheduleCreate] = inputs[0].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        for schedule in created_schedule_list:
            messenger = messenger_registry.get_messenger(schedule.messenger)
            job = get_job(
                JobGetQueryParams(
                    query_type=JobQueryType.GET_JOBS_BY_ID, job_id=schedule.job_id
                ),
                user,
            )
            message = Message(data=job, msg_type=MessageType.TO_DEMON_SCHEDULE_MSG)
            messenger.publish(message, schedule.messenger_queue)
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=created_schedule_list, description="List of created schedule Objects")
    ]


def generate_create_schedule_flow(
    schedule_create_request_list: List[Job], user: User
) -> Flow:
    """Generate flow for creating the schedule resource.

    Args:
        schedule_create_request_list (List[ScheduleCreate]): List of schedule create objects.
        user (User): User credentials.

    Returns:
        Flow: Create schedule flow
    """
    create_schedule_with_scheduler_step = Step(
        create_schedule_with_scheduler, dummy_backward
    )
    create_db_entry_step = Step(create_schedule_db_entry, revert_schedule_db_entry)
    publish_schedule_message_step = Step(publish_schedule_message, dummy_backward)

    flow = Flow()

    flow.add_step(
        create_schedule_with_scheduler_step,
        [
            Prop(
                data=schedule_create_request_list,
                description="List of schedule create request objects",
            ),
            Prop(data=user, description="User"),
        ],
    )

    create_db_entry_step_func_prop = FuncProp(
        func=flow.get_froward_output,
        params={"index": 0},
        description="Created schedule create object list",
    )
    flow.add_step(
        create_db_entry_step,
        [
            create_db_entry_step_func_prop,
            Prop(data=user, description="User"),
        ],
    )

    publish_schedule_message_step_func_prop = FuncProp(
        func=flow.get_froward_output,
        params={"index": 1},
        description="Created schedule list",
    )
    flow.add_step(
        publish_schedule_message_step,
        [
            publish_schedule_message_step_func_prop,
            Prop(data=user, description="User"),
        ],
    )

    return flow
