"""Slurm interface."""

from os import makedirs
from pathlib import Path
from typing import List

from demon.cluster.base import BaseCluster
from demon.schemas.job import Job
from demon.utils.command import call_cli

from xdg import xdg_data_home


class SlurmCluster(BaseCluster):
    """Slurm interface."""

    def prepare_job(self: "SlurmCluster", job: Job) -> None:
        """Prepare job for submission.

        Args:
            job (Job): Job object
        """
        job_data_path: Path = (
            xdg_data_home() / "orchestra" / "demon" / "jobs" / str(job.job_id)
        )  # noqa: E501
        makedirs((job_data_path / "out"), exist_ok=True)
        with open(job_data_path.joinpath("start.sh"), "w+") as f:
            f.write(job.script)

    def submit_job(self: "SlurmCluster", job: Job) -> str:
        """Submit job to the cluster.

        Args:
            job (Job): Job Object

        Returns:
            str: Job ID
        """
        self.prepare_job(job)
        job_data_path: Path = (
            xdg_data_home()
            / "orchestra"
            / "demon"
            / "jobs"
            / str(job.job_id)
            / "start.sh"  # noqa: E501
        )
        job_script_path: Path = job_data_path / "start.sh"
        job_out_path: Path = job_data_path / "out"
        cmd_args_list = [
            "sbatch",
            job_script_path.absolute(),
            "-o",
            job_out_path.absolute(),
        ]
        output = call_cli(cmd_args_list)
        submit_job_id = output.split(" ")[-1]
        return submit_job_id

    def get_job_status(self: "SlurmCluster", job_id: str) -> List[str]:
        """Get status of a job by Job.

        Args:
            job_id (str): ID of the job

        Returns:
            List[str]: List of status of the jobs
        """
        cmd_args_list = [
            "sacct",
            "-S",
            "1970-01-02",
            "--format",
            "State,ExitCode",
            "-j",
            job_id,
        ]
        output = call_cli(cmd_args_list)
        job_status_list = [status for status in output.strip().split("\n")[2:]]
        return job_status_list
