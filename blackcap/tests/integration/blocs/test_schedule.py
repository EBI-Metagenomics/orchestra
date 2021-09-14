"""Schedule BloCs integration tests."""
# flake8: noqa

from typing import Dict

from conductor.blocs.schedule import (
    create_schedule,
    delete_schedule,
    get_schedules,
    update_schedule,
)
from conductor.extentions import scheduler
from conductor.models.schedule import ScheduleDB
from conductor.schemas.api.schedule.delete import ScheduleDelete
from conductor.schemas.api.schedule.get import ScheduleGetQueryParams, ScheduleQueryType
from conductor.schemas.api.schedule.post import ScheduleCreate
from conductor.schemas.api.schedule.put import ScheduleUpdate
from conductor.schemas.job import Job
from conductor.schemas.schedule import Schedule
from conductor.schemas.user import User

from logzero import logger

from sqlalchemy import select
from sqlalchemy.orm.session import Session


def test_scheduler_schedule(
    user_dict: Dict, job_dict: Dict, db: Session, cluster_dict: Dict
) -> None:
    user = User(user_id=user_dict["id"], **user_dict)
    schedule = Schedule(
        user_id=user.user_id,
        job_id=job_dict["id"],
    )
    schedule_create_request = ScheduleCreate(user=user, schedule=schedule)
    created_schedule = scheduler.schedule(schedule_create_request)
    with db() as session:
        stmt = select(ScheduleDB)
        try:
            fetched_schedules = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(f"Unable to fetch schedules: {e}")
            raise e
        assert job_dict["id"] in [str(s.job_id) for s in fetched_schedules]
