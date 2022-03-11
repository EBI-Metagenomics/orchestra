"""Blackcap job POST route."""

from http import HTTPStatus
import json

from flask import make_response, request, Response
from pydantic import parse_obj_as, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from blackcap.blocs.cluster import create_cluster
from blackcap.routes.cluster import cluster_bp
from blackcap.schemas.api.cluster.post import ClusterPOSTRequest, ClusterPOSTResponse
from blackcap.schemas.user import User
from blackcap.utils.auth import check_authentication


@cluster_bp.post("/")
@check_authentication
def post(user: User) -> Response:
    """Post cluster.

    Args:
        user (User): Extracted user from request

    Returns:
        Response: Flask response
    """
    # Parse json from request
    try:
        cluster_create_request_list = parse_obj_as(
            ClusterPOSTRequest, json.loads(request.data)
        ).cluster_list
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
        cluster_list = create_cluster(cluster_create_request_list, user)
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
