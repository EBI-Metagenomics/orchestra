"""Blackcap job GET route."""

from http import HTTPStatus

from blackcap.blocs.job import get_jobs
from blackcap.routes.job import job_bp
from blackcap.schemas.api.job.get import JobGetQueryParams, JobGetResponse

from flask import Response, make_response, request

from pydantic.error_wrappers import ValidationError

from sqlalchemy.exc import SQLAlchemyError


@job_bp.get("/")
def get_job() -> Response:
    """Get job.

    Returns:
        Response: Flask response
    """
    # Parse query params from request
    try:
        query_params = JobGetQueryParams.parse_obj(request.args)
    except ValidationError as e:
        response_body = JobGetResponse(
            msg="query validation error", errors=e.errors()
        )  # noqa: E501
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = JobGetResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # Get jobs from the DB
    try:
        jobs = get_jobs(query_params)
    except SQLAlchemyError:
        response_body = JobGetResponse(
            msg="internal databse error", errors=["internal database error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501
    except Exception:
        response_body = JobGetResponse(
            msg="unknown error", errors=["unknown internal error"]
        )
        return make_response(
            response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR
        )  # noqa: E501

    # return fetched jobs in response
    response_body = JobGetResponse(
        msg="job successfully retrieved", items=jobs
    )  # noqa: E501
    return make_response(response_body.json(), HTTPStatus.OK)
