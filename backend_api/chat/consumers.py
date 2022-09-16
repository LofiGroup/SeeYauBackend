import json
from django.db.models import ObjectDoesNotExist
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models.models import ChatMessage, get_all_chats, ChatRoom, ChatUser
from profile.models import Profile
from .schemas import chat_message_to_dict
from utils.utils import current_time_in_millis


class WebsocketRequest:
    CHAT_MESSAGE: str = "chat_message"
    MARK_CHAT_AS_READ: str = "mark_chat_as_read"


class WebsocketResponse:
    CHAT_MESSAGE: str = "chat_message"
    CHAT_IS_READ: str = "chat_is_read"
    ERROR: str = "error"


class WebsocketError:
    def __init__(self, error_message: str):
        self.error_message: str = error_message


chat_access_error = WebsocketError(error_message=f"Chat does not exist or you don't have access to this chat.")


@database_sync_to_async
def save_message(chat_id, user, message):
    try:
        chat = ChatRoom.objects.get(pk=chat_id)
    except ObjectDoesNotExist:
        return chat_access_error

    if not chat.users.filter(pk=user.pk).exists():
        return chat_access_error

    message = chat.messages.create(message=message, author=user)
    return message


@database_sync_to_async
def mark_chat_as_read(chat_id, user):
    try:
        chat = ChatRoom.objects.get(pk=chat_id)
        read_in = current_time_in_millis()
        chat.chatusers.filter(user=user).update(read_in=read_in)
        return read_in
    except ObjectDoesNotExist:
        return chat_access_error


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
        print(f"Disconnecting from websocket... Code: {code}")
        for room_group_name in self.room_group_names:
            await self.channel_layer.group_discard(
                room_group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        print(f"Received data: {text_data}")
        text_data_json = json.loads(text_data)
        request_type = text_data_json['type']
        user = self.scope['user']

        match request_type:
            case WebsocketRequest.CHAT_MESSAGE:
                await self.on_chat_message_received(text_data_json)
            case WebsocketRequest.MARK_CHAT_AS_READ:
                await self.mark_as_read(text_data_json, user)
            case _:
                await self.send_error_response(f"Unknown request: {request_type}")

    async def mark_as_read(self, data, user):
        chat_id = data['chat_id']

        print(f"User marked chat {chat_id} as read")
        result = await mark_chat_as_read(chat_id, user)

        if self.request_is_invalid(result, int):
            return

        await self.channel_layer.group_send(
            f'chat_{chat_id}',
            {
                'type': 'response',
                'response_type': WebsocketResponse.CHAT_IS_READ,
                'chat_id': chat_id,
                'user_id': user.pk,
                'read_in': result
            }
        )

    async def on_chat_message_received(self, data):
        message = data['message']
        chat_id = data['chat_id']

        print(f"Received message: {message}, for chat: {chat_id}")

        message = await save_message(chat_id, self.scope['user'], message)

        if await self.request_is_invalid(message, ChatMessage):
            return

        await self.channel_layer.group_send(
            f'chat_{chat_id}',
            {
                'type': 'response',
                'response_type': WebsocketResponse.CHAT_MESSAGE,
                'chat_id': chat_id,
                'message': chat_message_to_dict(message)
            }
        )

    async def request_is_invalid(self, result, target_class=None):
        if result is WebsocketError:
            await self.send_error_response(result.error_message)
            return True
        elif target_class is not None and not isinstance(result, target_class):
            await self.send_error_response("Unknown error while sending message")
            return True
        return False

    async def send_error_response(self, message):
        await self.send(text_data=json.dumps({
            'type': WebsocketResponse.ERROR,
            'error_message': message
        }))

    async def response(self, event):
        await self.send(text_data=json.dumps(
            event
        ))
