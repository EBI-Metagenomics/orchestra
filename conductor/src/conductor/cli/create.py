"""Conductor create commands."""
# flake8: noqa

import click

from conductor import global_config, DBSession
from conductor.blocs.cluster import create_cluster
from conductor.blocs.job import create_job
from conductor.blocs.schedule import create_schedule
from conductor.blocs.user import create_user
from conductor.extentions import auther
from conductor.models.protagonist import ProtagonistDB
from conductor.schemas.api.cluster.post import ClusterCreate
from conductor.schemas.api.job.post import JobCreate
from conductor.schemas.api.schedule.post import ScheduleCreate
from conductor.schemas.api.user.post import UserCreate
from conductor.schemas.cluster import Cluster
from conductor.schemas.job import Job
from conductor.schemas.schedule import Schedule
from conductor.schemas.user import User

from logzero import logger

from sqlalchemy import select


@click.command()
@click.option("--email", required=True, help="email of the user")
@click.option("--password", required=True, help="password of the user")
@click.option("--name", default="CLI User", help="name of the user")
@click.option("--org", default="EBI", help="organisation of the user")
def user(email, password, name, org) -> None:
    """Create a user."""
    user_create_request = UserCreate(
        user=User(name=name, email=email, organisation=org), password=password
    )
    created_user_list = create_user([user_create_request])
    click.secho(f"User successfully created!\n\n{created_user_list[0]}", fg="green")


@click.command()
@click.option("--name", required=True, help="name of the cluster")
@click.option("--cluster_type", required=True, help="type of cluster")
@click.option("--cluster_caps", default="CPU", help="caps of cluster")
@click.option("--messenger", default="GCP", help="messenger the cluster uses")
@click.option("--queue", default="test-topic", help="messenger topic the cluster uses")
def cluster(name, cluster_type, cluster_caps, messenger, queue) -> None:
    """Create cluster."""
    # fetch a user first
    user_access_token = global_config.USER_ACCESS_TOKEN
    user = auther.extract_user_from_token(user_access_token)

    cluster_create_request = ClusterCreate(
        cluster=Cluster(
            name=name,
            cluster_type=cluster_type,
            cluster_caps=cluster_caps,
            messenger=messenger,
            messenger_queue=queue,
        ),
        user=user,
    )

    created_cluster_list = create_cluster([cluster_create_request])
    click.secho(f"User successfully created!\n\n{created_cluster_list[0]}", fg="green")


@click.group()
def create() -> None:
    """Create resources."""
    pass


create.add_command(user)
