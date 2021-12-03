"""Slurm interface."""

from os import makedirs
from pathlib import Path
from typing import List

from blackcap.cluster.base import BaseCluster
from blackcap.schemas.schedule import Schedule
from blackcap.utils.cli_commands import call_cli

from xdg import xdg_data_home


class SlurmCluster(BaseCluster):
    """Slurm interface."""

    CONFIG_KEY_VAL = "SLURM"

    def prepare_job(self: "SlurmCluster", schedule: Schedule) -> None:
        """Prepare job for submission.

        Args:
            schedule (Schedule): Schedule Object
        """
        job = schedule.job
        job_data_path: Path = (
            xdg_data_home() / "orchestra" / "demon" / "jobs" / str(job.job_id)
        )  # noqa: E501
        makedirs((job_data_path / "out"), exist_ok=True)
        with open(job_data_path.joinpath("start.sh"), "w+") as f:
            f.write(job.script)
        with open(job_data_path.joinpath("notify_start.sh"), "w+") as f:
            f.write(
                f"""#! /bin/bash
                conda activate orchestra

                demon pub schedup --sched_id={schedule.schedule_id} --job_id={job.job_id} --status=RUNNING  # noqa: E501
                """
            )
        with open(job_data_path.joinpath("notify_ok.sh"), "w+") as f:
            f.write(
                f"""#! /bin/bash
                conda activate orchestra

                demon pub schedup --sched_id={schedule.schedule_id} --job_id={job.job_id} --status=COMPLETED  # noqa: E501
                """
            )
        with open(job_data_path.joinpath("notify_not_ok.sh"), "w+") as f:
            f.write(
                f"""#! /bin/bash
                conda activate orchestra

                demon pub schedup --sched_id={schedule.schedule_id} --job_id={job.job_id} --status=FAILED  # noqa: E501
                """
            )

    def submit_job(self: "SlurmCluster", schedule: Schedule) -> str:
        """Submit job to the cluster.

        Args:
            schedule (Schedule): Schedule Object

        Returns:
            str: Job ID
        """
        job = schedule.job
        self.prepare_job(schedule)
        job_data_path: Path = (
            xdg_data_home()
            / "orchestra"
            / "demon"
            / "jobs"
            / str(job.job_id)  # noqa: E501
        )
        job_script_path: Path = job_data_path / "start.sh"
        # notify_start_script_path: Path = job_data_path / "notify_start.sh"
        # notify_ok_script_path: Path = job_data_path / "notify_ok.sh"
        # notify_not_ok_script_path: Path = job_data_path / "notify_not_ok.sh"
        job_out_path: Path = job_data_path / "out"
        main_job_cmd_args_list = [
            "sbatch",
            job_script_path.absolute(),
            "-o",
            job_out_path.absolute(),
        ]
        output = call_cli(main_job_cmd_args_list)

        # example: Submitted batch job 45
        main_job_id = output.split(" ")[-1]
        # TODO: Fix notify scripts
        # Add notify jobs
        # notify_start_job_cmd_args_list = [
        #     "sbatch",
        #     f"--dependency=after:{main_job_id}",
        #     notify_start_script_path.absolute(),
        #     "-o",
        #     job_out_path.absolute(),
        # ]
        # call_cli(notify_start_job_cmd_args_list)

        # notify_ok_job_cmd_args_list = [
        #     "sbatch",
        #     f"--dependency=afterok:{main_job_id}",
        #     notify_ok_script_path.absolute(),
        #     "-o",
        #     job_out_path.absolute(),
        # ]
        # call_cli(notify_ok_job_cmd_args_list)

        # notify_not_ok_job_cmd_args_list = [
        #     "sbatch",
        #     f"--dependency=afternotok:{main_job_id}",
        #     notify_not_ok_script_path.absolute(),
        #     "-o",
        #     job_out_path.absolute(),
        # ]
        # call_cli(notify_not_ok_job_cmd_args_list)
        return main_job_id

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
