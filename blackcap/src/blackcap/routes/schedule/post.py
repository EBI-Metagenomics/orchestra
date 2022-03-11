"""Blackcap schedule POST route."""

from http import HTTPStatus


from flask import make_response, request, Response
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.schedule import create_schedule
from blackcap.routes.schedule import schedule_bp
from blackcap.schemas.api.schedule.post import ScheduleCreate, SchedulePOSTResponse
from blackcap.schemas.user import User
from blackcap.utils.auth import check_authentication


@schedule_bp.post("/")
@check_authentication
def post_schedule(user: User) -> Response:
    """Post schedule.

    Args:
        user (User): Extracted user from request

    Returns:
        Response: Flask response
    """
    # Parse json from request
    try:
        schedule_create_request_list = ScheduleCreate.parse_obj(request.json)
    except ValidationError as e:
        response_body = SchedulePOSTResponse(
            msg="json validation failed", errors={"main": e.errors()}
        )
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = SchedulePOSTResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # ceate schedule in DB and publish msg
    try:
        schedule_list = create_schedule(schedule_create_request_list, user)
    except SQLAlchemyError:
        response_body = SchedulePOSTResponse(
            msg="internal databse error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        response_body = SchedulePOSTResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # return created schedule in response
    response_body = SchedulePOSTResponse(
        msg="schedule successfully created", items={"schedule_list": schedule_list}
    )
    return make_response(response_body.json(), HTTPStatus.OK)
