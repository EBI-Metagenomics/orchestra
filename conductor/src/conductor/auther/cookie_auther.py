"""Cookie Auther implementation of Auther."""


from conductor.auther.base import BaseAuther


class CookieAuther(BaseAuther):
    """Cookie Auther."""

    def register_user(self: "BaseAuther") -> None:
        return super().register_user()
