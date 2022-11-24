from app.websocket.base_consumer import Method
from chat.schemas import ChatMessageRead


class NotifyChatGroupMethod(Method):
    type = "notify_chat_group"
    response_type = "new_message"

    @staticmethod
    async def process(consumer, data: dict):
        chat_id = data['chat_id']

        await consumer.send_to_group_excluding_sender(
            f'chat_{chat_id}',
            {
                'type': NotifyChatGroupMethod.response_type,
                'message': data
            }
        )
