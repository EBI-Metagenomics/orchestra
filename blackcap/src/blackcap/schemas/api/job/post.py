"""Blackcap Job POST route schemas."""

from typing import Any, Dict, List, Optional, Union


from pydantic import BaseModel

from blackcap.schemas.job import Job


class JobCreate(BaseModel):
    """Schema to parse create job requests."""

    name: str
    description: Optional[str]
    job_type: str = ""
    specification: Dict = {}
    job_metadata: Dict = {}
    script: Optional[str]


class JobPOSTRequest(BaseModel):
    """Job POST request schema."""

    job_list: List[JobCreate]


class JobPOSTResponse(BaseModel):
    """Job POST response schema."""

    items: Dict[str, List[Union[Job, Any]]] = {}
