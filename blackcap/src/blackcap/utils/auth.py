"""Auth utils."""

from functools import wraps
from http import HTTPStatus
import sys
from typing import Callable

import click
from flask import make_response, request

from blackcap.auther import auther_registry
from blackcap.configs import config_registry
from blackcap.configs.base import BaseConfig
from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.user import User

config = config_registry.get_config()


def check_auth(config: BaseConfig) -> User:
    """Check authorization in CLI.

    Args:
        config (BaseConfig): config object

    Returns:
        User: User object
    """
    user_access_token = config.USER_ACCESS_TOKEN
    auther = auther_registry.get_auther(config.AUTHER)
    try:
        user = auther.extract_user_from_token(user_access_token)
    except Exception:
        click.secho("Authorization failed\n\n Exiting....")
        sys.exit(1)
    if user is None:
        click.secho("Authorization failed\n\n Exiting....")
        sys.exit(1)
    return user


def check_authentication(flask_route: Callable) -> Callable:
    """Decorator to check authentication in flask routes.

    Args:
        flask_route (Callable): Flask route

    Returns:
        Callable: Flask route
    """

    @wraps(flask_route)
    def wrapper() -> Callable:
        """Flask route wrapper.

        Returns:
            Callable: Flask route or Authentication error
        """
        # Extract token from cookie
        # Cookie example:
        # {"imcloud": "Bearer ey0038295.8kjfdfkd.kjfslusnv"}
        try:
            token_from_cookie = request.cookies.get("imcloud").split(" ")[1]
            # Try to extract user from token
            user = auther_registry.get_auther(config.AUTHER).extract_user_from_token(
                token_from_cookie
            )
            # Return Authentication error if user is none
            if user is None:
                raise Exception("User not found")
        except Exception:
            response_body = ResponseSchema(
                msg="Authentication failed. Please login again.",
                errors={
                    "main": [
                        {
                            "loc": "creds",
                            "msg": "unauthorized",
                            "type": "authentication",
                        }
                    ]
                },
            )
            return make_response(response_body.json(), HTTPStatus.UNAUTHORIZED)

        # Return flask route if auth is successful
        return flask_route(user)

    return wrapper
