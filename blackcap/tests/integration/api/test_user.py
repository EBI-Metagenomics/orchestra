"""User API tests."""
# flake8: noqa

from blackcap.schemas.api.user.post import UserCreate, UserPOSTRequest
from blackcap.schemas.user import User

from flask import Flask

from uuid import uuid4


def test_user_post(app: Flask) -> None:
    user_uuid = uuid4()
    user_create_json = UserPOSTRequest(
        users=[
            UserCreate(
                user=User(
                    user_id=user_uuid,
                    name="Tony Stark",
                    organisation="Stark Industries",
                    email="tony@stark.com",
                ),
                password="thisispass",
            )
        ]
    ).json()
    response = app.post("/v1/user/", json=user_create_json)
    print(response.data)
    assert response.status_code == 200
