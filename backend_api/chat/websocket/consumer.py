from channels.db import database_sync_to_async

from chat.models.crud import get_all_chats
from .methods import methods, NotifyUserOnlineStatusChangedMethod, OnlineStatus

from app.websocket.base_consumer import Consumer


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


class ChatConsumer(Consumer):
    ctype = "chat"
    methods = methods

    def __init__(self):
        super().__init__()
        self.chat_group_names = []

    async def on_connect(self):
        user = self.scope['user']
        chats = await get_user_chat_rooms(user)
        self.chat_group_names.extend(chats)

        for room_name in self.chat_group_names:
            await self.channel_layer.group_add(room_name, self.channel_name)

        await NotifyUserOnlineStatusChangedMethod.process(self, OnlineStatus.ONLINE)

    async def on_disconnect(self):
        await NotifyUserOnlineStatusChangedMethod.process(self, OnlineStatus.OFFLINE)
        for room_group_name in self.chat_group_names:
            await self.channel_layer.group_discard(room_group_name, self.channel_name)
