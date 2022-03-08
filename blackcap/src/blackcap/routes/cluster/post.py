"""Blackcap job POST route."""

from http import HTTPStatus
import json

from flask import make_response, request, Response
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.cluster import create_cluster
from blackcap.routes.cluster import cluster_bp
from blackcap.schemas.api.cluster.post import ClusterCreate, ClusterPOSTResponse


@cluster_bp.post("/")
def post() -> Response:
    """Post cluster.

    Returns:
        Response: Flask response
    """
    # Parse json from request
    try:
        cluster_create = ClusterCreate.parse_obj(json.loads(request.json))
    except ValidationError as e:
        response_body = ClusterPOSTResponse(
            msg="json validation failed", errors={"main": e.errors()}
        )
        return make_response(response_body.json(), HTTPStatus.BAD_REQUEST)
    except Exception:
        response_body = ClusterPOSTResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # ceate cluster in DB and publish msg
    try:
        cluster_list = create_cluster(cluster_create)
    except SQLAlchemyError:
        response_body = ClusterPOSTResponse(
            msg="internal databse error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        response_body = ClusterPOSTResponse(
            msg="unknown error", errors={"main": ["unknown internal error"]}
        )
        return make_response(response_body.json(), HTTPStatus.INTERNAL_SERVER_ERROR)

    # return created cluster in response
    response_body = ClusterPOSTResponse(
        msg="cluster successfully created", items={"cluster_list": cluster_list}
    )
    return make_response(response_body.json(), HTTPStatus.OK)
