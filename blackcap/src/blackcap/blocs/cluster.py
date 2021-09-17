"""Cluster BLoCs."""

from typing import List

from blackcap.db import DBSession
from blackcap.models.cluster import ClusterDB
from blackcap.schemas.api.cluster.get import (
    ClusterGetQueryParams,
    ClusterQueryType,
)  # noqa: E501
from blackcap.schemas.api.cluster.post import ClusterCreate
from blackcap.schemas.cluster import Cluster

from logzero import logger

from sqlalchemy import select


def create_cluster(
    cluster_create_list: List[ClusterCreate],
) -> List[Cluster]:  # noqa: E501
    """Create clusters from create cluster request.

    Args:
        cluster_create_list (List[ClusterCreate]): ClusterCreate request

    Raises:
        Exception: error

    Returns:
        List[Cluster]: List of created clusters
    """
    with DBSession() as session:
        try:
            cluster_db_create_list: List[ClusterDB] = [
                ClusterDB(
                    **cluster_create.cluster.dict(exclude={"cluster_id"})
                )  # noqa: E501
                for cluster_create in cluster_create_list
            ]
            ClusterDB.bulk_create(cluster_db_create_list, session)
            return [
                Cluster(cluster_id=obj.id, **obj.to_dict())
                for obj in cluster_db_create_list
            ]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to create clusters: {e}")
            raise e


def get_clusters(query_params: ClusterGetQueryParams) -> List[Cluster]:
    """Query DB for clusters.

    Args:
        query_params (ClusterGetQueryParams): Query params from request

    Raises:
        Exception: error

    Returns:
        List[Cluster]: List of clusters returned from DB
    """
    cluster_list: List[ClusterDB] = []

    stmt = ""

    if query_params.query_type == ClusterQueryType.GET_ALL_CLUSTER:
        stmt = select(ClusterDB)

    with DBSession() as session:
        try:
            cluster_list: List[ClusterDB] = (
                session.execute(stmt).scalars().all()
            )  # noqa: E501
            return [
                Cluster(cluster_id=obj.id, **obj.to_dict())
                for obj in cluster_list  # noqa: E501
            ]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch clusters due to {e}")
            raise e
