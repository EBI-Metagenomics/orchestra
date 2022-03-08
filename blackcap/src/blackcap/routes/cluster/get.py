"""Blackcap job GET route."""

from http import HTTPStatus

from flask import make_response, request, Response
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.cluster import get_cluster
from blackcap.routes.cluster import cluster_bp
from blackcap.schemas.api.cluster.get import ClusterGetQueryParams, ClusterGetResponse


@cluster_bp.get("/")
def get() -> Response:
    """Get cluster.

    Returns:
        Response: Flask response
    """
    # Parse query params from request
    try:
        query_params = ClusterGetQueryParams.parse_obj(request.args)
    except ValidationError as e:
        response_body = ClusterGetResponse(
            msg="query validation error", errors={"main": e.errors()}
        )
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = ClusterGetResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # Get cluster list from the DB
    try:
        cluster_list = get_cluster(query_params)
    except SQLAlchemyError:
        response_body = ClusterGetResponse(
            msg="internal databse error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        response_body = ClusterGetResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # return fetched cluster list in response
    response_body = ClusterGetResponse(
        msg="cluster list successfully retrieved", items={"cluster_list": cluster_list}
    )
    return make_response(response_body.json(), HTTPStatus.OK)
