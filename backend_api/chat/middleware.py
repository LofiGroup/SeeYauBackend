from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from ninja.errors import HttpError
from .models.crud import get_chat_room, user_in_chat

no_such_room = HttpError(status_code=404, message="No such room")
no_access_to_room = HttpError(status_code=401, message="No access to room")


class ChatRoomMiddleWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            query = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
            room_name = query.get('room_name', "")
        except ValueError:
            room_name = ""
        room = await database_sync_to_async(get_chat_room)(room_name)
        if room is None:
            raise no_such_room
        user = scope['user']
        if not await database_sync_to_async(user_in_chat)(user, room):
            raise no_access_to_room

        scope['chat_room'] = room
        return await self.app(scope, receive, send)
