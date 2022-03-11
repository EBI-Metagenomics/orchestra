"""Protagonist model tests."""
# flake8: noqa

from bcrypt import gensalt, hashpw
from logzero import logger
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from blackcap.models.protagonist import ProtagonistDB


def test_get_all_users(db: Session) -> None:
    passwd = hashpw("random_key".encode(), gensalt())
    user = ProtagonistDB(
        name="test_user_1",
        email="test_email_1@gmail.com",
        password=passwd,
    )

    with db() as session:
        user.save(session)
        stmt = select(ProtagonistDB)
        try:
            fetched_users = session.execute(stmt).scalars().all()
        except Exception as e:
            logger.error(f"Unable tofetch user: {e}")
            raise e
        assert user.id in [str(u.id) for u in fetched_users]


def test_get_by_email(db: Session) -> None:
    passwd = hashpw("random_key".encode(), gensalt())
    user = ProtagonistDB(
        name="test_user",
        email="test_email",
        password=passwd,
    )

    with db() as session:
        user.save(session)
        stmt = select(ProtagonistDB).where(ProtagonistDB.email == "test_email")
        try:
            fetched_user = session.execute(stmt).scalars().all()[0]
        except Exception as e:
            logger.error(f"Unable tofetch user: {e}")
            raise e
        assert fetched_user.name == user.name
        assert fetched_user.password == user.password
