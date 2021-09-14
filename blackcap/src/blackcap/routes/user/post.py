"""Blackcap user POST route."""

import json
from http import HTTPStatus
from typing import List

from blackcap.blocs.user import create_user
from blackcap.routes.user import user_bp
from blackcap.schemas.api.user.post import (
    UserCreate,
    UserPOSTRequest,
    UserPOSTResponse,
)

from flask import Response, make_response, request

from pydantic import ValidationError, parse_obj_as

from sqlalchemy.exc import SQLAlchemyError


@user_bp.post("/")
def post_user() -> Response:
    """Post User.

    Returns:
        Response: Flask response
    """
    # Parse json from request
    try:
        user_post_request = UserPOSTRequest.parse_obj(json.loads(request.json))
        user_create_list = parse_obj_as(
            List[UserCreate], user_post_request.users
        )  # noqa: E501
    except ValidationError as e:
        response_body = UserPOSTResponse(
            msg="json validation failed", errors=e.errors()
        )  # noqa: E501
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = UserPOSTResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # ceate user in DB

    try:
        user_list = create_user(user_create_list)
    except SQLAlchemyError:
        response_body = UserPOSTResponse(
            msg="internal databse error", errors=["internal database error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501
    except Exception:
        response_body = UserPOSTResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # return created users in response
    response_body = UserPOSTResponse(
        msg="users successfully created", items=user_list
    )  # noqa: E501
    return make_response(response_body.json(), HTTPStatus.OK)
