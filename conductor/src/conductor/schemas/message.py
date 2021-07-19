"""Message schema."""

from enum import Enum, unique
from typing import Dict

from pydantic import BaseModel


@unique
class MessageType(Enum):
    """Message types."""

    TO_DEMON_SCHEDULE_MSG = "to_demon_schedule_msg"
    TO_CONDUCTOR_JOB_STATUS_UPDATE = "to_conductor_job_status_update"


class Message(BaseModel):
    """Message schema to serialize/deserialze messenger msgs."""

    msg_type: MessageType
    data: Dict
    timestamp: str
