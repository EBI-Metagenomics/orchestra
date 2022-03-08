"""Blackcap job POST route."""

from http import HTTPStatus
import json

from flask import make_response, request, Response
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.job import create_job
from blackcap.routes.job import job_bp
from blackcap.schemas.api.job.post import JobCreate, JobPOSTResponse


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
        job_list = create_job(job_create)
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
