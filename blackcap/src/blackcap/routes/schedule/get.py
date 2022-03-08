"""Blackcap schedule GET route."""

from http import HTTPStatus

from flask import make_response, request, Response
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.schedule import get_schedules
from blackcap.routes.schedule import schedule_bp
from blackcap.schemas.api.schedule.get import (
    ScheduleGetQueryParams,
    ScheduleGetResponse,
)


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
            msg="query validation error", errors={"main": e.errors()}
        )
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = ScheduleGetResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # Get s from the DB
    try:
        schedule_list = get_schedules(query_params)
    except SQLAlchemyError:
        response_body = ScheduleGetResponse(
            msg="internal databse error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        response_body = ScheduleGetResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # return fetched s in response
    response_body = ScheduleGetResponse(
        msg=" successfully retrieved", items={"schedule_list": schedule_list}
    )
    return make_response(response_body.json(), HTTPStatus.OK)
