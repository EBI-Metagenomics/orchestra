"""Message schema."""

from enum import Enum, unique
from typing import Dict

from pydantic import BaseModel, validator


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

    @validator("msg_type")
    def convert_msg_type_enum_to_str(cls: "Message", v: MessageType) -> str:
        """Convert enum to str.

        Args:
            v (MessageType): MessageType Enum

        Returns:
            str: string value of enum
        """
        return v.value
