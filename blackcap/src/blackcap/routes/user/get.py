"""Blackcap user GET route."""

from http import HTTPStatus

from blackcap.blocs.user import get_users
from blackcap.routes.user import user_bp
from blackcap.schemas.api.user.get import UserGetQueryParams, UserGetResponse

from flask import Response, make_response, request

from pydantic.error_wrappers import ValidationError

from sqlalchemy.exc import SQLAlchemyError


@user_bp.get("/")
def get_user() -> Response:
    """Get user.

    Returns:
        Response: Flask response
    """
    # Parse query params from request
    try:
        query_params = UserGetQueryParams.parse_obj(request.args)
    except ValidationError as e:
        response_body = UserGetResponse(
            msg="query validation error", errors=e.errors()
        )  # noqa: E501
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = UserGetResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # Get users from the DB
    try:
        user_list = get_users(query_params)
    except SQLAlchemyError:
        response_body = UserGetResponse(
            msg="internal databse error", errors=["internal database error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501
    except Exception:
        response_body = UserGetResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # return fetched users in response
    response_body = UserGetResponse(
        msg=" successfully retrieved", items=user_list
    )  # noqa: E501
    return make_response(response_body.json(), HTTPStatus.OK)
