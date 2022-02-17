"""Blackcap Job PUT route schemas."""

from typing import Any, Dict, List, Union

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.job import Job


class JobUpdate(BaseModel):
    """Schema to parse update job requests."""

    job_id: UUID4


class JobPUTRequest(BaseModel):
    """Job PUT request schema."""

    job_list: List[JobUpdate]


class JobPUTResponse(BaseModel):
    """Job PUT response schema."""

    items: Dict[str, List[Union[Job, Any]]] = {}
