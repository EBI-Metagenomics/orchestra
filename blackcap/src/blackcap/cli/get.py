"""Blackcap get commands."""
# flake8: noqa

import click

from blackcap.blocs.user import get_users
from blackcap.schemas.api.user.get import UserGetQueryParams, UserQueryType
from blackcap.schemas.user import User


@click.command()
@click.option("--type", required=True, help="type of the user query")
@click.option("--email", help="email of the user")
@click.option("--password", help="password of the user")
@click.option("--name", help="name of the user")
@click.option("--org", help="organisation of the user")
def user(type, email, password, name, org) -> None:
    """Get a user"""
    query_param = UserGetQueryParams(
        query_type=UserQueryType(type), name=name, email=email, organisation=org
    )
    fetched_user_list = get_users(query_param)
    click.secho(f"Users successfully fetched!\n\n", fg="green")
    for user in fetched_user_list:
        click.secho(f"{str(user.id)}, {user.name}, {user.email}, {user.organisation}")


@click.group()
def get() -> None:
    """Get resources."""
    pass


get.add_command(user)
