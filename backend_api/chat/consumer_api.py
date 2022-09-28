from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


def notify_new_chat_is_created(user, chat_id: int):
    async_to_sync(channel_layer.group_send)(f"user_{user.pk}", {"type": "connect_to_new_chat", "chat_id": chat_id})

