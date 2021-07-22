"""Pub/Sub callbacks for Slurm."""

import json
import os
import uuid
from typing import Union

from demon.extentions import DBSession
from demon.clusters.slurm import SlurmCluster
from demon.schemas.job import Job
from demon.schemas.jobs.base import BaseJob, BaseJobDB
from demon.schemas.message import Message

from google.cloud.pubsub_v1.subscriber.message import Message as GCPMessage


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
        job_id = SlurmCluster().submit_job(job_file=os.path.abspath(f.name))
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
        job_id = SlurmCluster().submit_job(job_file=os.path.abspath(f.name))
        print(job_id)
    msg.ack()


def save_job_from_msg(msg: GCPMessage) -> None:
    """Save jobs to DB from Pub/Sub msgs.

    Args:
        msg (GCPMessage): Pub/Sub Msg
    """
    parsed_msg = Message.parse_raw(msg.data)
    job = Job(**parsed_msg.data)
    jobdb = BaseJobDB(**job.dict())
    with DBSession() as session:
        jobdb.save(session)
    msg.ack()
