"""Blackcap job POST route."""

import json
from http import HTTPStatus

from blackcap.blocs.job import create_job
from blackcap.routes.job import job_bp
from blackcap.schemas.api.job.post import JobCreate, JobPOSTResponse

from flask import Response, make_response, request

from pydantic import ValidationError

from sqlalchemy.exc import SQLAlchemyError


@job_bp.post("/")
def post_job() -> Response:
    """Post job.

    Returns:
        Response: Flask response
    """
    # Parse json from request
    try:
        job_create = JobCreate.parse_obj(json.loads(request.json))
    except ValidationError as e:
        response_body = JobPOSTResponse(
            msg="json validation failed", errors=e.errors()
        )  # noqa: E501
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = JobPOSTResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # ceate job in DB and publish msg
    try:
        job = create_job(job_create)
    except SQLAlchemyError:
        response_body = JobPOSTResponse(
            msg="internal databse error", errors=["internal database error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501
    except Exception:
        response_body = JobPOSTResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # return created job in response
    response_body = JobPOSTResponse(
        msg="job successfully created", items=[job.dict()]
    )  # noqa: E501
    return make_response(response_body.json(), HTTPStatus.OK)
