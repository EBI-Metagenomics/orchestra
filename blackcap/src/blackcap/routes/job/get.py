"""Blackcap job GET route."""

from http import HTTPStatus

from flask import make_response, request, Response
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.job import get_jobs
from blackcap.routes.job import job_bp
from blackcap.schemas.api.job.get import JobGetQueryParams, JobGetResponse


@job_bp.get("/")
def get() -> Response:
    """Get job.

    Returns:
        Response: Flask response
    """
    # Parse query params from request
    try:
        query_params = JobGetQueryParams.parse_obj(request.args)
    except ValidationError as e:
        response_body = JobGetResponse(
            msg="query validation error", errors={"main": e.errors()}
        )
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = JobGetResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # Get jobs from the DB
    try:
        job_list = get_jobs(query_params)
    except SQLAlchemyError:
        response_body = JobGetResponse(
            msg="internal databse error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        response_body = JobGetResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # return fetched jobs in response
    response_body = JobGetResponse(
        msg="job successfully retrieved", items={"job_list": job_list}
    )
    return make_response(response_body.json(), HTTPStatus.OK)
