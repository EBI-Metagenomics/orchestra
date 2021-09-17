"""Random Scheduler implementation of Scheduler."""

import random
from typing import List

from blackcap.db import DBSession
from blackcap.models.cluster import ClusterDB
from blackcap.models.schedule import ScheduleDB
from blackcap.scheduler.base import BaseScheduler
from blackcap.schemas.api.schedule.post import ScheduleCreate
from blackcap.schemas.schedule import Schedule

from logzero import logger

from sqlalchemy.sql.expression import select


class RandomScheduler(BaseScheduler):
    """Random scheduler schedule jobs randomly."""

    CONFIG_KEY_VAL = "RANDOM"

    def schedule(
        self: "BaseScheduler", schedule_create: ScheduleCreate
    ) -> Schedule:  # noqa: E501
        """Create schedule from schedule request.

        Args:
            schedule_create (ScheduleCreate): Schedule create request

        Raises:
            Exception: No cluster available

        Returns:
            Schedule: Instance of Created Schedule
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
        schedule_dict = schedule_create.schedule.dict(
            exclude={"schedule_id", "messenger", "messenger_queue", "job"}
        )
        user_id = schedule_dict.pop("user_id")
        try:
            schedule = ScheduleDB(
                protagonist_id=user_id,
                **schedule_dict,
            )
            schedule.save(session)
            return Schedule(
                schedule_id=schedule.id,
                user_id=user_id,
                messenger=selected_cluster.messenger,
                messenger_queue=selected_cluster.messenger_queue,
                job=schedule_create.schedule.job,
                **schedule.to_dict(),
            )
        except Exception as e:
            logger.error(f"Unable to save schedule to DB: {e}")
            raise e
