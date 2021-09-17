"""Blackcap create commands."""
# flake8: noqa

from pathlib import Path
import click

from blackcap.auther import auther_registry
from blackcap.blocs.cluster import create_cluster
from blackcap.blocs.job import create_job, get_jobs, JobGetQueryParams, JobQueryType
from blackcap.blocs.schedule import create_schedule
from blackcap.blocs.user import create_user
from blackcap.configs import config_registry
from blackcap.schemas.api.cluster.post import ClusterCreate
from blackcap.schemas.api.job.post import JobCreate
from blackcap.schemas.api.schedule.post import ScheduleCreate
from blackcap.schemas.api.user.post import UserCreate
from blackcap.schemas.cluster import Cluster
from blackcap.schemas.job import Job
from blackcap.schemas.schedule import Schedule
from blackcap.schemas.user import User

config = config_registry.get_config()


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
    user_access_token = config.USER_ACCESS_TOKEN
    auther = auther_registry.get_auther(config.AUTHER)
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
    click.secho(
        f"Cluster successfully created!\n\n{created_cluster_list[0]}", fg="green"
    )


@click.command()
@click.option("--name", required=True, help="name of the job")
@click.option("--script", required=True, help="path of the script")
def job(name, script) -> None:
    """Create cluster."""
    # fetch a user first
    user_access_token = config.USER_ACCESS_TOKEN
    auther = auther_registry.get_auther(config.AUTHER)
    user = auther.extract_user_from_token(user_access_token)
    script_path = Path(script)
    with open(script_path) as script_file:
        script_content = script_file.read()
    job_create_request = JobCreate(
        job=Job(name=name, script=script_content),
        user=user,
    )
    created_job_list = create_job([job_create_request])
    click.secho(f"Job successfully created!\n\n{created_job_list[0]}", fg="green")


@click.command()
@click.option("--job_id", required=True, help="id of the job")
def schedule(job_id) -> None:
    """Create cluster."""
    # fetch a user first
    user_access_token = config.USER_ACCESS_TOKEN
    auther = auther_registry.get_auther(config.AUTHER)
    user = auther.extract_user_from_token(user_access_token)

    fetched_jobs = get_jobs(
        JobGetQueryParams(query_type=JobQueryType.GET_JOBS_BY_ID, job_id=job_id)
    )
    if len(fetched_jobs) == 0:
        click.secho(f"Job with id {job_id} not found!", fg="red")
    else:
        schedule_create_request = ScheduleCreate(
            schedule=Schedule(job_id=job_id, user_id=user.user_id, job=fetched_jobs[0]),
            user=user,
        )
        created_schedule_list = create_schedule([schedule_create_request])
        click.secho(
            f"Schedule successfully created!\n\n{created_schedule_list[0]}", fg="green"
        )


@click.group()
def create() -> None:
    """Create resources."""
    pass


create.add_command(user)
create.add_command(cluster)
create.add_command(job)
create.add_command(schedule)
