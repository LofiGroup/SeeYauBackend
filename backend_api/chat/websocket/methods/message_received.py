from channels.db import database_sync_to_async

from chat.models.models import ChatMessage
from chat.models.crud import save_chat_message
from app.websocket.base_consumer import Method, WebsocketError
from chat.schemas import ChatMessageCreate, ChatMessageRead

access_error = WebsocketError("Access error")


@database_sync_to_async
def save_message(user, message_data: ChatMessageCreate):
    message = save_chat_message(user, message_data)
    if message is None:
        return access_error

    return message


class MessageReceivedMethod(Method):
    type = "chat_message"
    response_type = "new_message"

    sender_response_type = "message_is_received"

    @staticmethod
    async def process(consumer, data: dict):
        create_message = ChatMessageCreate.parse_obj(data)

        print(f"Received message: {create_message.message}, for chat: {create_message.chat_id}")
        message: ChatMessage = await save_message(consumer.scope['user'], create_message)

        if await consumer.request_is_invalid(message, ChatMessage):
            return

        await consumer.send_to_group_excluding_sender(
            f'chat_{create_message.chat_id}',
            {
                'type': MessageReceivedMethod.response_type,
                'message': ChatMessageRead.from_orm(message).dict()
            }
        )

        await consumer.send({
            'type': MessageReceivedMethod.sender_response_type,
            'local_id': create_message.local_id,
            'real_id': message.pk,
            'created_in': message.created_in
        })
