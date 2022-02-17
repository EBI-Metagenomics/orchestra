"""Blackcap Job DELETE route schemas."""

from typing import Any, Dict, List, Union

from pydantic import UUID4, BaseModel

from blackcap.schemas.job import Job


class JobDelete(BaseModel):
    """Schema to parse delete job requests."""

    job_id: UUID4


class JobPUTRequest(BaseModel):
    """Job PUT request schema."""

    job_list: List[JobDelete]


class JobPUTResponse(BaseModel):
    """Job PUT response schema."""

    items: Dict[str, List[Union[Job, Any]]] = {}
