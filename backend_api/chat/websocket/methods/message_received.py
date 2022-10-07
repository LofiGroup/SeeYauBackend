from channels.db import database_sync_to_async
from django.db.models import ObjectDoesNotExist

from chat.models.models import ChatMessage, ChatRoom
from chat.schemas import chat_message_to_dict
from app.websocket.base_consumer import Method, WebsocketError

access_error = WebsocketError("Access error")


@database_sync_to_async
def save_message(chat_id, user, message):
    try:
        chat = ChatRoom.objects.get(pk=chat_id)
    except ObjectDoesNotExist:
        return access_error

    if not chat.users.filter(pk=user.pk).exists():
        return access_error

    message = chat.messages.create(message=message, author=user)
    return message


class MessageReceivedMethod(Method):
    type = "chat_message"
    response_type = "new_message"

    @staticmethod
    async def process(consumer, data: dict):
        message = data['message']
        chat_id = data['chat_id']

        print(f"Received message: {message}, for chat: {chat_id}")

        message = await save_message(chat_id, consumer.scope['user'], message)

        if await consumer.request_is_invalid(message, ChatMessage):
            return

        await consumer.send_to_group(
            f'chat_{chat_id}',
            {
                'type': MessageReceivedMethod.response_type,
                'chat_id': chat_id,
                'message': chat_message_to_dict(message)
            }
        )
