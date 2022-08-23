import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models.models import ChatMessage, get_all_chats, ChatRoom


@database_sync_to_async
def save_message(chat_room_id, user, message):
    chat = ChatRoom.objects.get(pk=chat_room_id)
    chat.messages.create(message=message, author=user)


@database_sync_to_async
def get_user_chat_rooms(user):
    chats = []
    chat_rooms = get_all_chats(user)
    print("user chats:")
    for chat in chat_rooms:
        room_name = "chat_%s" % chat.pk
        chats.append(room_name)
        print("\t" + room_name)
    return chats


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_names = []

    async def connect(self):
        print("Connecting to websocket...")
        await self.accept()
        user = self.scope['user']
        chats = await get_user_chat_rooms(user)
        self.room_group_names.extend(chats)

        for room_name in self.room_group_names:
            await self.channel_layer.group_add(room_name, self.channel_name)
        print("Successfully connected to websocket!")

    async def disconnect(self, code):
        print("Disconnecting from websocket...")
        for room_group_name in self.room_group_names:
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat_room_id = text_data_json['chat_room_id']
        print(f"Received message: {message}, for chat: {chat_room_id}")

        await self.channel_layer.group_send(
            f'chat_{chat_room_id}',
            {
                'type': 'chat_message',
                'chat_room_id': chat_room_id,
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        chat_room_id = event['chat_room_id']

        await save_message(chat_room_id, self.scope['user'], message)
        await self.send(text_data=json.dumps({
            'chat_room_id': chat_room_id,
            'message': message
        }))
