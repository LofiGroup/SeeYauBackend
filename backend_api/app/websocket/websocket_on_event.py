from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

app_channel_layer = get_channel_layer()


def on_event(user_id: int, data: dict):
    async_to_sync(app_channel_layer.group_send)(f"user_{user_id}", {"type": "on_event", "data": data})
