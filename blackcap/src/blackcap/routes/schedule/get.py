"""Blackcap schedule GET route."""

from http import HTTPStatus

from blackcap.blocs.schedule import get_schedules
from blackcap.routes.schedule import schedule_bp
from blackcap.schemas.api.schedule.get import (
    ScheduleGetQueryParams,
    ScheduleGetResponse,
)

from flask import Response, make_response, request

from pydantic.error_wrappers import ValidationError

from sqlalchemy.exc import SQLAlchemyError


@schedule_bp.get("/")
def get_schedule() -> Response:
    """Get schedule.

    Returns:
        Response: Flask response
    """
    # Parse query params from request
    try:
        query_params = ScheduleGetQueryParams.parse_raw(request.query_string)
    except ValidationError as e:
        response_body = ScheduleGetResponse(
            msg="query validation error", errors=e.errors()
        )  # noqa: E501
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = ScheduleGetResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # Get s from the DB
    try:
        schedules = get_schedules(query_params)
    except SQLAlchemyError:
        response_body = ScheduleGetResponse(
            msg="internal databse error", errors=["internal database error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501
    except Exception:
        response_body = ScheduleGetResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # return fetched s in response
    response_body = ScheduleGetResponse(
        msg=" successfully retrieved", items=schedules
    )  # noqa: E501
    return make_response(response_body.json(), HTTPStatus.OK)
