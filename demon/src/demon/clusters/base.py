"""Base cluster inteface."""

from abc import ABC, abstractmethod
from typing import List

from demon.schemas.jobs.base import BaseJob, JobStatus


class BaseCluster(ABC):
    """Base cluster interface."""

    @abstractmethod
    def submit_job(self: "BaseCluster", job: BaseJob) -> str:
        """Submit job to the cluster.

        Args:
            job (BaseJob): A Job object

        Returns:
            str: Job ID
        """
        pass

    def get_job_status(self: "BaseCluster", job_id: str) -> List[JobStatus]:
        """Get status of a job by Job.

        Args:
            job_id (str): ID of the job

        Returns:
            List[JobStatus]: List of  status of the jobs # noqa DAR202
        """
        pass
