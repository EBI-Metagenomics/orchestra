"""Blackcap Schedule GET route schemas."""

from enum import Enum, unique
from typing import List, Optional

from blackcap.schemas.api.common import ResponseSchema
from blackcap.schemas.schedule import Schedule

from pydantic import BaseModel


class ScheduleGetQueryParams(BaseModel):
    """Schedule GET request query params schema."""

    schedule_id: Optional[str]
    job_id: Optional[str]
    protagonist_id: Optional[str]
    cluster_id: Optional[str]
    create_timerange: Optional[str]
    finished_timerange: Optional[str]


class ScheduleGetResponse(ResponseSchema):
    """Schedule GET response schema."""

    items: List[Schedule] = []


@unique
class ScheduleQueryType(Enum):
    """Schedule Query type enum."""

    GET_ALL_SCHEDULES = "get_all_schedules"
    GET_SCHEDULE_BY_ID = "get_schedule_by_id"
    GET_SCHEDULES_BY_PROTAGONIST_ID = "get_schedules_by_protagonist_id"
    GET_SCHEDULES_BY_CLUSTER_ID = "get_schedules_by_cluster_id"
    GET_SCHEDULES_BY_CREATE_TIMERANGE = "get_schedules_by_create_timerange"
    GET_SCHEDULES_BY_FINISHED_TIMERANGE = "get_schedules_by_finished_timerange"
