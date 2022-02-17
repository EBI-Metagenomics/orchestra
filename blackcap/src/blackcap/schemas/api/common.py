"""Blackcap common schemas."""

from typing import Any, Dict, List

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    """API response schema."""

    msg: str
    items: Dict[str, List[Any]] = {}
    errors: Dict[str, List[Any]] = {}
