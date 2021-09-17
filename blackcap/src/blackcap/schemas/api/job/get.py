"""Blackcap Job GET route schemas."""

from enum import Enum, unique
from typing import List, Optional

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.job import Job

from pydantic import BaseModel


class JobGetResponse(ResponseSchema):
    """Job GET response schema."""

    items: List[Job] = []


@unique
class JobQueryType(Enum):
    """Job Query type enum."""

    GET_ALL_JOBS = "get_all_jobs"
    GET_JOBS_BY_ID = "get_job_by_id"
    GET_JOBS_BY_PROTAGONIST_ID = "get_jobs_by_protagonist_id"
    GET_JOBS_BY_CLUSTER_ID = "get_jobs_by_cluster_id"
    GET_JOBS_BY_CREATE_TIMERANGE = "get_jobs_by_create_timerange"
    GET_JOBS_BY_FINISHED_TIMERANGE = "get_jobs_by_finished_timerange"
    GET_JOBS_BY_STATUS = "get_jobs_by_status"


class JobGetQueryParams(BaseModel):
    """Job GET request query params schema."""

    query_type: JobQueryType
    job_id: Optional[str]
    protagonist_id: Optional[str]
    cluster_id: Optional[str]
    create_timerange: Optional[str]
    finished_timerange: Optional[str]
    job_status: Optional[str]
