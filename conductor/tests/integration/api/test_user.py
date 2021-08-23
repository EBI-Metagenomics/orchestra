"""User API tests."""
# flake8: noqa

from conductor.schemas.api.user.post import UserCreate, UserPOSTRequest
from conductor.schemas.user import User

from flask import Flask

from uuid import uuid4


def test_user_post(app: Flask) -> None:
    with app.test_client() as test_client:
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
        response = test_client.post("/v1/user/", json=user_create_json)
        print(response.data)
        assert response.status_code == 200
