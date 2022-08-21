import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models.models import ChatMessage


@database_sync_to_async
def send_message(chat, user, message):
    chat.messages.create(message=message, author=user.profile)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = ""

    async def connect(self):
        print("Connecting to websocket...")
        room_name = self.scope['chat_room'].pk
        self.room_group_name = 'chat_%s' % room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("Successfully connected to websocket!")

    async def disconnect(self, code):
        print("Disconnecting from websocket...")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await send_message(self.scope['chat_room'], self.scope['user'], message)
        await self.send(text_data=json.dumps({
            'message': message
        }))
