"""Job model tests."""
# flake8: noqa

from typing import Dict

from logzero import logger
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from blackcap.models.job import JobDB


def test_get_all_jobs(db: Session, user_dict: Dict) -> None:

    job = JobDB(
        name="very cool job",
        script="#! /bin/bash\n\n/bin/hostname\nsrun -l /bin/hostname\nsrun -l /bin/hostname\n",  # noqa: E501
        cluster_caps_req="CPU",
        protagonist_id=user_dict["id"],
    )
    with db() as session:
        job.save(session)
        stmt = select(JobDB)
        try:
            fetched_jobs = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(f"Unable to fetch jobs: {e}")
            raise e
        assert job.id in [str(j.id) for j in fetched_jobs]
