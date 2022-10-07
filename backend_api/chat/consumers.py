import json
from enum import Enum

from django.db.models import ObjectDoesNotExist
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models.models import ChatMessage, get_all_chats, ChatRoom, ChatUser
from profile.models import Profile
from .schemas import chat_message_to_dict
from utils.utils import current_time_in_millis, IS_ONLINE


class WebsocketRequest:
    CHAT_MESSAGE: str = "chat_message"
    MARK_CHAT_AS_READ: str = "mark_chat_as_read"


class WebsocketResponse:
    CHAT_MESSAGE: str = "chat_message"
    CHAT_IS_READ: str = "chat_is_read"
    USER_ONLINE_STATUS_CHANGED: str = "online_status_changed"
    NEW_CHAT_IS_CREATED: str = "new_chat_is_created"
    ERROR: str = "error"


class OnlineStatus(Enum):
    OFFLINE = 0
    ONLINE = 1


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


@database_sync_to_async
def set_user_online_status(user: Profile, status: OnlineStatus):
    if status is OnlineStatus.OFFLINE:
        user.last_seen = current_time_in_millis()
    else:
        user.last_seen = IS_ONLINE
    user.save()


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_group_names = []
        self.user_room = ""

    async def connect(self):
        print("Connecting to websocket...")
        await self.accept()
        user = self.scope['user']
        self.user_room = f"user_{user.pk}"

        chats = await get_user_chat_rooms(user)
        self.chat_group_names.extend(chats)

        await self.channel_layer.group_add(self.user_room, self.channel_name)

        for room_name in self.chat_group_names:
            await self.channel_layer.group_add(room_name, self.channel_name)
        print("Successfully connected to websocket!")

        await self.notify_online_status_changed(status=OnlineStatus.ONLINE)

    async def disconnect(self, code):
        print(f"Disconnecting from websocket... Code: {code}")

        await self.notify_online_status_changed(status=OnlineStatus.OFFLINE)

        await self.channel_layer.group_discard(self.user_room, self.channel_name)

        for room_group_name in self.chat_group_names:
            await self.channel_layer.group_discard(room_group_name, self.channel_name)

    async def notify_online_status_changed(self, status: OnlineStatus):
        user: Profile = self.scope['user']
        await set_user_online_status(user, status)
        print(f"User status is changed: user_id: {user.pk}")

        for room_group_name in self.chat_group_names:
            await self.send_to_chat(
                room_group_name,
                {
                    'type': WebsocketResponse.USER_ONLINE_STATUS_CHANGED,
                    'user_id': user.pk
                }
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

        result = await mark_chat_as_read(chat_id, user)

        if await self.request_is_invalid(result, int):
            return

        await self.send_to_chat(
            f'chat_{chat_id}',
            {
                'type': WebsocketResponse.CHAT_IS_READ,
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

        await self.send_to_chat(
            f'chat_{chat_id}',
            {
                'type': WebsocketResponse.CHAT_MESSAGE,
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

    async def connect_to_new_chat(self, event):
        chat_id = event['chat_id']
        room_name = f"chat_{chat_id}"

        self.chat_group_names.append(room_name)
        await self.channel_layer.group_add(room_name, self.channel_name)

        await self.send(text_data=json.dumps({
            'type': "chat",
            "data": {
                "type": WebsocketResponse.NEW_CHAT_IS_CREATED,
                "chat_id": chat_id
            }
        }))

    async def send_to_chat(self, room_name, data):
        await self.channel_layer.group_send(
            room_name,
            {
                "type": "chat",
                "data": data
            }
        )

    async def chat(self, event):
        print(f"Sending through websocket: {event}")
        await self.send(text_data=json.dumps(
            event
        ))
