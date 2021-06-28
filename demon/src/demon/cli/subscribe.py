"""subscribe commands."""
# flake8: noqa: DAR101

import random
from pathlib import Path

import click

from demon.utils.slurm_callbacks import submit_job_from_msg
from demon.utils.subscribe import echo_msg, subscribe_topic

from logzero import logger


@click.command()
@click.option("--id", default="test-sub", help="Subscription Id")
def echo(id: str) -> None:
    """subscribe and echo msgs"""
    logger.info("Trying to subscribe and read messages...")
    try:
        subscribe_topic(sub_id=id, callback=echo_msg)
    except Exception as e:
        logger.error(f"failed to subscribe: {e}")


@click.command()
@click.option("--id", default="test-sub", help="Subscription Id")
def slurm(id: str) -> None:
    """subscribe and submit msgs to slurm"""
    logger.info("Trying to subscribe and read messages...")
    try:
        subscribe_topic(sub_id=id, callback=submit_job_from_msg)
    except Exception as e:
        logger.error(f"failed to subscribe: {e}")


@click.group()
def sub() -> None:
    """GCP pub/sub channel subscribe commands."""
    pass


sub.add_command(echo)
sub.add_command(slurm)