"""Cluster model tests."""
# flake8: noqa

from logzero import logger
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from blackcap.models.cluster import ClusterDB


def test_get_all_clusters(db: Session) -> None:

    cluster = ClusterDB(
        name="EBI_Embassy_01",
        cluster_type="SLURM",
        status="ACTIVE",
        cluster_caps="CPU,GPU",
        messenger="GCP",
        messenger_queue="test-topic",
    )
    with db() as session:
        cluster.save(session)
        stmt = select(ClusterDB)
        try:
            fetched_clusters = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(f"Unable to fetch clusters: {e}")
            raise e
        assert cluster.id in [str(c.id) for c in fetched_clusters]
