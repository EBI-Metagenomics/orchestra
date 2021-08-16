"""Random Scheduler implementation of Scheduler."""

import random
from typing import List

from conductor import DBSession
from conductor.models.cluster import ClusterDB
from conductor.models.schedule import ScheduleDB
from conductor.scheduler.base import BaseScheduler
from conductor.schemas.api.schedule.post import ScheduleCreate

from logzero import logger

from sqlalchemy.sql.expression import select


class RandomScheduler(BaseScheduler):
    """Random scheduler schedule jobs randomly."""

    def schedule(
        self: "BaseScheduler", schedule_create: ScheduleCreate
    ) -> ScheduleDB:  # noqa: E501
        """Create schedule from schedule request.

        Args:
            schedule_create (ScheduleCreate): Schedule create request

        Raises:
            Exception: No cluster available

        Returns:
            ScheduleDB: Instance of ScheduleDB
        """
        # fetch available clusters
        cluster_list: List[ClusterDB] = []
        with DBSession() as session:
            try:
                stmt = select(ClusterDB)
                cluster_list = session.execute(stmt).scalars().all()  # noqa: E501
            except Exception as e:
                logger.error(f"Unable to fetch clusters: {e}")
                raise e

        # Raise error if no cluster available
        if len(cluster_list) == 0:
            logger.error("No cluster available")
            raise Exception("cluster_list: List[ClusterDB]")

        # Randomly selects a cluster
        selected_cluster = random.choice(cluster_list)  # noqa: S311

        schedule_create.schedule.assigned_cluster_id = selected_cluster.id

        # Add schedule to DB
        schedule_dict = schedule_create.schedule.dict()
        user_id = schedule_dict.pop("user_id")
        try:
            schedule = ScheduleDB(
                protagonist_id=user_id,
                **schedule_dict,
            )
            schedule.save(session)
            return schedule
        except Exception as e:
            logger.error(f"Unable to save schedule to DB: {e}")
            raise e
