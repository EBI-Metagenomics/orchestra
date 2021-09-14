"""Schedule commands."""
# flake8: noqa: DAR101

from pathlib import Path

import click

from blackcap.blocs.job import create_job
from blackcap.schemas.api.job.post import JobCreate
from blackcap.schemas.job import Job

from logzero import logger


@click.command()
@click.option("--file", help="file path of job's JSON file", required=True)
def random(file: str) -> None:
    """Schedule a job."""
    logger.info("Trying to schedule the job...")
    try:
        job_file_path = Path(file)
        with open(job_file_path) as job_file:
            data = job_file.read()
            job = Job.parse_raw(data)
            job_create = JobCreate(job=job)
            created_job = create_job(job_create)
            logger.info(f"\nSuccess!\nJob: {created_job}")
    except Exception as e:
        logger.error(f"failed to schedule the job: {e}")
        raise e


@click.group()
def sched() -> None:
    """Schedule jobs."""
    pass


sched.add_command(random)
