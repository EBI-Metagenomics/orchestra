"""Blackcap job POST route."""

from http import HTTPStatus
import json

from flask import make_response, request, Response
from pydantic import parse_obj_as, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.job import create_job
from blackcap.routes.job import job_bp
from blackcap.schemas.api.job.post import JobPOSTRequest, JobPOSTResponse
from blackcap.schemas.user import User
from blackcap.utils.auth import check_authentication


@job_bp.post("/")
@check_authentication
def post_job(user: User) -> Response:
    """Post job.

    Args:
        user (User): Extracted user from request

    Returns:
        Response: Flask response
    """
    # Parse json from request
    try:
        job_create_request_list = parse_obj_as(
            JobPOSTRequest, json.loads(request.data)
        ).job_list
    except ValidationError as e:
        response_body = JobPOSTResponse(
            msg="json validation failed", errors={"main": e.errors()}
        )
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = JobPOSTResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # ceate job in DB and publish msg
    try:
        job_list = create_job(job_create_request_list, user)
    except SQLAlchemyError:
        response_body = JobPOSTResponse(
            msg="internal databse error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        response_body = JobPOSTResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # return created job in response
    response_body = JobPOSTResponse(
        msg="job successfully created", items={"job_list": job_list}
    )
    return make_response(response_body.json(), HTTPStatus.OK)
