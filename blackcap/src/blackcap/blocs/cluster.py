"""Cluster BLoCs."""

from typing import List

from logzero import logger
from sqlalchemy import select

from blackcap.db import DBSession
from blackcap.models.cluster import ClusterDB
from blackcap.schemas.api.cluster.delete import ClusterDelete
from blackcap.schemas.api.cluster.get import (
    ClusterGetQueryParams,
    ClusterQueryType,
)
from blackcap.schemas.api.cluster.post import ClusterCreate
from blackcap.schemas.api.cluster.put import ClusterUpdate
from blackcap.schemas.cluster import Cluster
from blackcap.schemas.user import User


def create_cluster(
    cluster_create_list: List[ClusterCreate], user_creds: User
) -> List[Cluster]:
    """Create clusters from create cluster request.

    Args:
        cluster_create_list (List[ClusterCreate]): ClusterCreate request list
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        List[Cluster]: List of created clusters
    """
    with DBSession() as session:
        try:
            cluster_db_create_list: List[ClusterDB] = [
                ClusterDB(**cluster_create.cluster.dict())
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


def get_clusters(
    query_params: ClusterGetQueryParams, user_creds: User
) -> List[Cluster]:
    """Query DB for clusters.

    Args:
        query_params (ClusterGetQueryParams): Query params from request
        user_creds (User): User credentials.

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
            cluster_list: List[ClusterDB] = session.execute(stmt).scalars().all()
            return [Cluster(cluster_id=obj.id, **obj.to_dict()) for obj in cluster_list]
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to fetch clusters due to {e}")
            raise e


def update_cluster(
    cluster_update_list: List[ClusterUpdate], user_creds: User
) -> List[Cluster]:
    """Update cluster in the DB from ClusterUpdate request.

    Args:
        cluster_update_list (List[ClusterUpdate]): List of ClusterUpdate request
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        List[Cluster]: List of Instance of Updated Cluster
    """
    stmt = (
        select(ClusterDB)
        .where(ClusterDB.protagonist_id == user_creds.user_id)
        .where(
            ClusterDB.id.in_(
                [cluster_update.template_id for cluster_update in cluster_update_list]
            )
        )
    )
    with DBSession() as session:
        try:
            cluster_db_update_list: List[ClusterDB] = (
                session.execute(stmt).scalars().all()
            )
            updated_cluster_list = []
            for cluster in cluster_db_update_list:
                for cluster_update in cluster_update_list:
                    if cluster_update.cluster_id == cluster.id:
                        cluster_update_dict = cluster_update.dict(exclude_defaults=True)
                        cluster_update_dict.pop("cluster_id")
                        updated_cluster = cluster.update(session, **cluster_update_dict)
                        updated_cluster_list.append(
                            Cluster(
                                cluster_id=updated_cluster.id,
                                **updated_cluster.to_dict(),
                            )
                        )
            return updated_cluster_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to update cluster: {cluster.to_dict()} due to {e}")
            raise e


def delete_cluster(
    cluster_delete_list: List[ClusterDelete], user_creds: User
) -> List[Cluster]:
    """Delete cluster in the DB from ClusterDelete request.

    Args:
        cluster_delete_list (List[ClusterDelete]): List of ClusterDelete request
        user_creds (User): User credentials.

    Raises:
        Exception: error

    Returns:
        List[Cluster]: List of Instance of Deleted Cluster
    """
    stmt = (
        select(ClusterDB)
        .where(ClusterDB.protagonist_id == user_creds.user_id)
        .where(
            ClusterDB.id.in_([cluster.cluster_id for cluster in cluster_delete_list])
        )
    )
    with DBSession() as session:
        try:
            cluster_db_delete_list: List[ClusterDB] = (
                session.execute(stmt).scalars().all()
            )
            deleted_cluster_list = []
            for cluster in cluster_db_delete_list:
                cluster.delete(session)
                deleted_cluster_list.append(
                    Cluster(cluster_id=cluster.id, **cluster.to_dict())
                )
            return deleted_cluster_list
        except Exception as e:
            session.rollback()
            logger.error(f"Unable to delete cluster: {cluster.to_dict()} due to {e}")
            raise e
