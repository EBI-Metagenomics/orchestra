"""GCP implementation of messenger."""

import json
from typing import Callable, Optional

from demon import DBSession
from demon.configs.base import BaseConfig
from demon.messenger.base import BaseMessenger
from demon.models.job import JobDB
from demon.models.schedule import ScheduleDB
from demon.schemas.message import Message, MessageType
from demon.schemas.schedule import Schedule
from demon.utils.json_encoders import UUIDEncoder


from google.auth import jwt
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message as GCPMessage

from sqlalchemy.sql.expression import select


class GCPMessenger(BaseMessenger):
    """GCP(Pub/Sub) implementation of Messenger."""

    def __init__(self: "GCPMessenger", config: BaseConfig) -> None:
        """Initialize Messenger with app config.

        Args:
            config (BaseConfig): Config to initialize messenger
        """
        self.pub_audience = (
            "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"  # noqa: E501
        )
        self.sub_audience = (
            "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"  # noqa: E501
        )
        self.service_account_info = json.load(
            open(config.GOOGLE_APPLICATION_CREDENTIALS)
        )  # noqa: E501
        self.pub_credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=self.pub_audience
        )

        self.sub_credentials = jwt.Credentials.from_service_account_info(
            self.service_account_info, audience=self.sub_audience
        )

        self.publisher = pubsub_v1.PublisherClient(
            credentials=self.pub_credentials
        )  # noqa: E501

        self.subscriber = pubsub_v1.SubscriberClient(
            credentials=self.sub_credentials
        )  # noqa: E501
        self.project_id = config.GCP_PROJECT_ID

    def publish(self: "GCPMessenger", msg: Message, topic_id: str) -> str:
        """Publish msg on the GCP Pub/Sub queue.

        Args:
            msg (Message): Messsag to publish
            topic_id (str): Id of the topic

        Returns:
            str: Id of the published msg
        """
        topic_path = self.publisher.topic_path(self.project_id, topic_id)

        # Msg must be a bytestring
        msg = json.dumps(msg, cls=UUIDEncoder).encode("utf-8")

        # Wait for the returned future
        future = self.publisher.publish(topic_path, msg)
        return future.result()

    def subscribe(
        self: "GCPMessenger",
        callback: Callable,
        sub_id: str,
        timeout: Optional[float] = None,  # noqa: E501
    ) -> None:
        """Subscribe to a topic.

        Args:
            callback (Callable): Callback to invoke when a msg is received
            sub_id (str): Id of the topic.
            timeout (Union[float, None]): Time to wait for msgs. Defaults to None. # noqa: E501
        """
        subscription_path = self.subscriber.subscription_path(
            self.project_id, sub_id
        )  # noqa: E501

        streaming_pull_future = self.subscriber.subscribe(
            subscription_path,
            callback=callback,
            await_callbacks_on_shutdown=True,  # noqa: E501
        )

        with self.subscriber:
            try:
                streaming_pull_future.result(timeout=timeout)
            except TimeoutError:
                streaming_pull_future.cancel()

    def process_schedule_msg(self: "GCPMessenger", msg: GCPMessage) -> None:
        """Process Schedule Pub/Sub msgs.

        Args:
            msg (GCPMessage): Pub/Sub Msg
        """
        parsed_msg = Message.parse_raw(msg.data)
        if parsed_msg.msg_type == MessageType.TO_DEMON_SCHEDULE_MSG:
            schedule = Schedule(**parsed_msg.data)
            # Check if job already exists
            stmt = select(JobDB).where(JobDB.id == schedule.job_id)
            with DBSession() as session:
                fetched_jobs = session.execute(stmt).scalars().all()
                if len(fetched_jobs) == 0:
                    # Create the job
                    jobdb = JobDB(
                        id=schedule.job_id,
                        **schedule.job.dict(exclude={"job_id"})  # noqa: E501
                    )
                    jobdb.save(session)
                # Create schedule
                scheduledb = ScheduleDB(
                    id=schedule.schedule_id,
                    job_id=schedule.job_id,
                    protagonist_id=schedule.user_id,
                )
                scheduledb.save(session)
            msg.ack()

    def echo_msg(self: "GCPMessenger", msg: Message) -> None:
        """Echo msgs to stdout.

        Args:
            msg (Message): Message to echo
        """
        print(msg)
        msg.ack()
