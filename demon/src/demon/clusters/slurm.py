"""Slurm interface."""

from typing import List

from demon.clusters.base import BaseCluster
from demon.schemas.jobs.base import JobStatus
from demon.utils.command import call_cli


class SlurmCluster(BaseCluster):
    """Slurm interface."""

    def submit_job(self: "BaseCluster", job_file: str) -> str:
        """Submit job to the cluster.

        Args:
            job_file (str): Path to job script

        Returns:
            str: Job ID
        """
        cmd_args_list = ["sbatch", job_file]
        output = call_cli(cmd_args_list)
        submit_job_id = output.split(" ")[-1]
        return submit_job_id

    def get_job_status(self: "BaseCluster", job_id: str) -> List[JobStatus]:
        """Get status of a job by Job.

        Args:
            job_id (str): ID of the job

        Returns:
            List[JobStatus]: List of status of the jobs
        """
        cmd_args_list = ["sacct", "--format", "State", "-j", job_id]
        output = call_cli(cmd_args_list)
        job_status_list = [
            JobStatus(status) for status in output.strip().split("\n")[2:]
        ]
        return job_status_list
