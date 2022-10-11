from enum import Enum
from channels.db import database_sync_to_async
from django.db.models import ObjectDoesNotExist

from chat.models.models import ChatRoom
from utils.utils import current_time_in_millis
from app.websocket.base_consumer import Method, WebsocketError


@database_sync_to_async
def mark_chat_as_read(chat_id, user):
    try:
        chat = ChatRoom.objects.get(pk=chat_id)
        read_in = current_time_in_millis()
        chat.chatusers.filter(user=user).update(read_in=read_in)
        return read_in
    except ObjectDoesNotExist:
        return WebsocketError("Access error")


class MarkChatAsReadMethod(Method):
    type = "mark_chat_as_read"
    response_type = "chat_is_read"

    @staticmethod
    async def process(consumer, data):
        user = consumer.scope['user']
        chat_id = data['chat_id']

        result = await mark_chat_as_read(chat_id, user)

        if await consumer.request_is_invalid(result, int):
            return

        await consumer.send_to_group(
            f'chat_{chat_id}',
            {
                'type': MarkChatAsReadMethod.response_type,
                'chat_id': chat_id,
                'user_id': user.pk,
                'read_in': result
            }
        )
