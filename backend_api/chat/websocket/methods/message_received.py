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

    sender_response_type = "message_is_received"

    @staticmethod
    async def process(consumer, data: dict):
        message = data['message']
        chat_id = data['chat_id']
        local_id = data['local_id']

        print(f"Received message: {message}, for chat: {chat_id}")

        message: ChatMessage = await save_message(chat_id, consumer.scope['user'], message)

        if await consumer.request_is_invalid(message, ChatMessage):
            return

        message_data = chat_message_to_dict(message)
        await consumer.send_to_group_excluding_sender(
            f'chat_{chat_id}',
            {
                'type': MessageReceivedMethod.response_type,
                'chat_id': chat_id,
                'message': message_data
            }
        )
        await consumer.send({
            'type': MessageReceivedMethod.sender_response_type,
            'local_id': local_id,
            'real_id': message.pk,
            'created_in': message.created_in
        })
