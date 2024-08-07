from enum import Enum
from channels.db import database_sync_to_async

from profile.models.profile import Profile, set_user_is_online, set_user_is_offline
from app.websocket.base_consumer import Method


class OnlineStatus(Enum):
    OFFLINE = 0
    ONLINE = 1


@database_sync_to_async
def set_user_online_status(user: Profile, status: OnlineStatus):
    if status is OnlineStatus.OFFLINE:
        set_user_is_offline(user.pk)
    else:
        set_user_is_online(user.pk)


class NotifyUserOnlineStatusChangedMethod(Method):
    type = "notify_online_status_changed"
    response_type = "online_status_changed"

    @staticmethod
    async def process(consumer, data):
        user: Profile = consumer.scope['user']

        await set_user_online_status(user, data)
        print(f"User status is changed: user_id: {user.pk}, status: {data}")

        for room_group_name in consumer.chat_group_names:
            await consumer.send_to_group_excluding_sender(
                room_group_name,
                {
                    'type': NotifyUserOnlineStatusChangedMethod.response_type,
                    'user_id': user.pk
                }
            )
