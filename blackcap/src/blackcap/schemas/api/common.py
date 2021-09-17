"""Blackcap common schemas."""

from typing import Any, List

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """API response schema."""

    msg: str
    items: List[Any] = []
    errors: List[Any] = []
