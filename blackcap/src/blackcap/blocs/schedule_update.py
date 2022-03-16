"""Schedule update BLoCs."""

from typing import Any

from logzero import logger

from blackcap.blocs.schedule import update_schedule
from blackcap.configs import config_registry
from blackcap.messenger import messenger_registry
from blackcap.schemas.api.schedule.put import ScheduleUpdate
from blackcap.schemas.user import User

config = config_registry.get_config()
messenger = messenger_registry.get_messenger(config.MESSENGER)


def process_schedule_update_msg(messenger_msg: Any) -> None:
    """Update DB with schedule updates."""
    try:
        schedule_update_request = ScheduleUpdate.parse_obj(
            messenger.parse_messenger_msg(messenger_msg).data
        )
        updated_schedule = update_schedule(
            [schedule_update_request],
            User(
                user_id=schedule_update_request.protagonist_id,
                name="",
                organisation="",
                email="",
            ),
        )[0]
        logger.info(updated_schedule.dict(exclude={"logs"}))
    except Exception as e:
        # Add central logging
        pass
