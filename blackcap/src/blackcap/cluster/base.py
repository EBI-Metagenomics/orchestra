"""Base cluster inteface."""

from abc import ABC, abstractmethod
from typing import List

from blackcap.schemas.schedule import Schedule


class BaseCluster(ABC):
    """Base cluster interface."""

    @abstractmethod
    def prepare_job(self: "BaseCluster", schedule: Schedule) -> None:
        """Prepare job for submission.

        Args:
            schedule (Schedule): Schedule Object
        """

    @abstractmethod
    def submit_job(self: "BaseCluster", schedule: Schedule) -> str:
        """Submit job to the cluster.

        Args:
            schedule (Schedule): Schedule Object

        Returns:
            str: Job ID
        """
        pass

    @abstractmethod
    def get_job_status(self: "BaseCluster", job_id: str) -> List[str]:
        """Get status of a job.

        Args:
            job_id (str): ID of the job

        Returns:
            List[str]: List of  status of the jobs
        """
        pass
