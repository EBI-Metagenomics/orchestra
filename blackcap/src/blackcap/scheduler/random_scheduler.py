"""Random Scheduler implementation of Scheduler."""

import random
from typing import List

from logzero import logger
from sqlalchemy.sql.expression import select

from blackcap.db import DBSession
from blackcap.models.cluster import ClusterDB
from blackcap.scheduler.base import BaseScheduler
from blackcap.schemas.api.schedule.post import ScheduleCreate


class RandomScheduler(BaseScheduler):
    """Random scheduler schedule jobs randomly."""

    CONFIG_KEY_VAL = "RANDOM"

    def schedule(
        self: "BaseScheduler", schedule_create: ScheduleCreate
    ) -> ScheduleCreate:
        """Create schedule from schedule request.

        Args:
            schedule_create (ScheduleCreate): Schedule create request

        Raises:
            Exception: No cluster available

        Returns:
            ScheduleCreate: Instance of Schedule Create
        """
        # fetch available clusters
        cluster_list: List[ClusterDB] = []
        with DBSession() as session:
            try:
                stmt = select(ClusterDB)
                cluster_list = session.execute(stmt).scalars().all()
            except Exception as e:
                logger.error(f"Unable to fetch clusters: {e}")
                raise e

        # Raise error if no cluster available
        if len(cluster_list) == 0:
            logger.error("No cluster available")
            raise Exception("cluster_list: List[ClusterDB]")

        # Randomly selects a cluster
        selected_cluster = random.choice(cluster_list)  # noqa: S311
        schedule_create.assigned_cluster_id = selected_cluster.id

        return schedule_create
