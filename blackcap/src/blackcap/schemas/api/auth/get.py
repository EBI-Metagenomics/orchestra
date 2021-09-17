"""Blackcap Auth GET route schemas."""

from pydantic import BaseModel


class AuthGetCredsReset(BaseModel):
    """Schema to parse user password reset request."""

    email: str
