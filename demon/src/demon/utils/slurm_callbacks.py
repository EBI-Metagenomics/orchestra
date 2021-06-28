"""Pub/Sub callbacks for Slurm."""

import json
import os
import uuid
from typing import Union

from demon.clusters.slurm import Slurm
from demon.schemas.jobs.base import BaseJob, BaseJobDB

from google.cloud.pubsub_v1.subscriber.message import Message


def submit_slurm_job(job: Union[BaseJobDB, BaseJob]) -> str:
    """Submit job to slurm.

    Args:
        job (Union[BaseJobDB, BaseJob]): Instance of job

    Returns:
        str: JobID
    """
    with open(f"{uuid.uuid4()}.json", "w+") as f:
        f.write(job.script)
        f.read()
        job_id = Slurm().submit_job(job_file=os.path.abspath(f.name))
        return job_id


def submit_job_from_msg(msg: Message) -> None:
    """Submit jobs to Slurm from Pub/Sub msgs.

    Args:
        msg (Message): Pub/Sub Msg
    """
    job_obj = json.loads(msg.data)
    job = BaseJob(**job_obj)
    with open(f"{uuid.uuid4()}.json", "w+") as f:
        f.write(job.script)
        print(f.read())
        job_id = Slurm().submit_job(job_file=os.path.abspath(f.name))
        print(job_id)
    msg.ack()


def save_job_from_msg(msg: Message) -> None:
    """Save jobs to DB from Pub/Sub msgs.

    Args:
        msg (Message): Pub/Sub Msg
    """
    job_obj = BaseJob.parse_raw(msg.data)
    job = BaseJobDB(**job_obj.dict())
    job.save()
    msg.ack()
