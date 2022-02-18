"""Blackcap Job DELETE route schemas."""

from typing import Any, Dict, List, Union

from pydantic import BaseModel, UUID4

from blackcap.schemas.job import Job


class JobDelete(BaseModel):
    """Schema to parse delete job requests."""

    job_id: UUID4


class JobDELETERequest(BaseModel):
    """Job DELETE request schema."""

    job_list: List[JobDelete]


class JobDELETEResponse(BaseModel):
    """Job DELETE response schema."""

    items: Dict[str, List[Union[Job, Any]]] = {}
