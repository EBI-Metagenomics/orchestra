"""Cluster BLoCs."""

from typing import List

from logzero import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from blackcap.db import DBSession
from blackcap.flow import Flow, FlowExecError, get_outer_function, Prop, Step
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


###
# Flow BLoCs
###


def create_cluster_db_entry(inputs: List[Prop]) -> List[Prop]:
    """Create cluster db entry step function.

    Args:
        inputs (List[Prop]):
            Expects
                0: cluster_create_request_list
                    Prop(data=cluster_create_request_list, description="List of create cluster objects")
                1: user
                    Prop(data=user, description="User")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Created cluster objects

            Prop(data=created_cluster_list, description="List of created cluster Objects")
    """
    try:
        cluster_create_request_list: List[ClusterCreate] = inputs[0].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        created_cluster_list = create_cluster(cluster_create_request_list, user)
    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Creating DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=created_cluster_list, description="List of created cluster Objects")
    ]


def revert_cluster_db_entry(inputs: List[Prop]) -> List[Prop]:
    """Delete db entry step function.

    Args:
        inputs (List[Prop]):
            Expects
                0: cluster_create_request_list
                    Prop(data=cluster_create_request_list, description="List of create cluster objects")
                1: user
                    Prop(data=user, description="User")
                2: created_cluster_list
                    Prop(data=created_data_list, description="List of created cluster objects")

    Raises:
        FlowExecError: Flow execution failed

    Returns:
        List[Prop]:
            Deleted data objects

            Prop(data=deleted_cluster_list, description="List of deleted cluster Objects")
    """
    try:
        created_cluster_list: List[Cluster] = inputs[2].data
        user: User = inputs[1].data
    except Exception as e:
        raise FlowExecError(
            human_description="Parsing inputs failed",
            error=e,
            error_type=type(e),
            is_user_facing=True,
            error_in_function=get_outer_function(),
        ) from e

    try:
        deleted_cluster_list = delete_cluster(created_cluster_list, user)
    except SQLAlchemyError as e:
        raise FlowExecError(
            human_description="Deleting DB object failed",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e
    except Exception as e:
        raise FlowExecError(
            human_description="Something bad happened",
            error=e,
            error_type=type(e),
            is_user_facing=False,
            error_in_function=get_outer_function(),
        ) from e

    return [
        Prop(data=deleted_cluster_list, description="List of deleted cluster Objects")
    ]


def generate_create_cluster_flow(
    cluster_create_request_list: List[ClusterCreate], user: User
) -> Flow:
    """Generate flow for creating the cluster resource.

    Args:
        cluster_create_request_list (List[ClusterCreate]): List of cluster objects to create.
        user (User): User credentials.

    Returns:
        Flow: Create cluster flow
    """
    create_db_entry_step = Step(create_cluster_db_entry, revert_cluster_db_entry)
    # create_messenger_topic_step = Step(create_messenger_topic, delete_meesenger_topic)

    flow = Flow()

    flow.add_step(
        create_db_entry_step,
        [
            Prop(
                data=cluster_create_request_list,
                description="List of ClusterCreate Objects",
            ),
            Prop(data=user, description="User"),
        ],
    )

    return flow
