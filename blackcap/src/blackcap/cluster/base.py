"""Base cluster inteface."""

from abc import ABC, abstractmethod
from typing import Any, List

from blackcap.configs import config_registry
from blackcap.messenger import messenger_registry
from blackcap.schemas.schedule import Schedule

config = config_registry.get_config()
messenger = messenger_registry.get_messenger(config.MESSENGER)


class BaseCluster(ABC):
    """Base cluster interface."""

    CONFIG_KEY = "CLUSTER"
    CONFIG_KEY_DEF_VAL = "ARGO"

    # Change this value in custom auther implementations.
    CONFIG_KEY_VAL = "ARGO"

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

    def process_schedule_msg(self: "BaseCluster", messenger_msg: Any) -> None:
        """Submit job to the cluster.

        Args:
            messenger_msg (Any): message in Messenger specific format
        """
        schedule = messenger.parse_messenger_msg(messenger_msg)
        self.prepare_job(schedule)
        self.submit_job(schedule)
