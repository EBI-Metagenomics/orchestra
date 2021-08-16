"""Schedule model tests."""
# flake8: noqa

from typing import Dict


from conductor.models.schedule import ScheduleDB

from logzero import logger

from sqlalchemy import select
from sqlalchemy.orm.session import Session


def test_get_all_schedules(
    db: Session, user_dict: Dict, job_dict: Dict, cluster_dict: Dict
) -> None:

    schedule = ScheduleDB(
        job_id=job_dict["id"],
        assigned_cluster_id=cluster_dict["id"],
        protagonist_id=user_dict["id"],
    )
    with db() as session:
        schedule.save(session)
        stmt = select(ScheduleDB)
        try:
            fetched_schedules = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(f"Unable to fetch schedules: {e}")
            raise e
        assert schedule.id in [str(s.id) for s in fetched_schedules]
