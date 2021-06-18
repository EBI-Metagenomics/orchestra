"""Pub/Sub callbacks for Slurm."""

import json
import tempfile

from demon.clusters.slurm import Slurm
from demon.jobs.base import BaseJob

from google.cloud.pubsub_v1.subscriber.message import Message


def submit_job_from_msg(msg: Message) -> None:
    """Submit jobs to Slurm from Pub/Sub msgs.

    Args:
        msg (Message): Pub/Sub Msg
    """
    job_obj = json.loads(msg.data)
    job = BaseJob(**job_obj)
    with tempfile.NamedTemporaryFile() as f:
        f.write(job.json().encode())
        job_id = Slurm().submit_job(job_file=f.name)
        print(job_id)
    msg.ack()
