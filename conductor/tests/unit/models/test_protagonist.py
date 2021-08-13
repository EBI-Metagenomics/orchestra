"""Protagonist model tests."""
# flake8: noqa

from bcrypt import gensalt, hashpw

from conductor.models.protagonist import ProtagonistDB

from logzero import logger

from sqlalchemy import select
from sqlalchemy.orm.session import Session


def test_get_by_email(db: Session) -> None:
    passwd = hashpw("random_key".encode(), gensalt())
    user = ProtagonistDB(
        name="test_user",
        email="test_email",
        password=passwd,
    )
    with db() as session:
        user.save(session)

    # recreate new session after saving as a workaround
    with db() as session:
        stmt = select(ProtagonistDB).where(ProtagonistDB.email == "test_email")
        try:
            fetched_user = session.execute(stmt).scalars().all()[0]
        except Exception as e:
            logger.error(f"Unable tofetch user: {e}")
            raise e
        assert fetched_user.name == user.name
        assert fetched_user.password == user.password
