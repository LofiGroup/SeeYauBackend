from .jwt_auth import validate_token, authentication_error
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(token):
    return validate_token(token).profile


class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            query = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
            token_key = query.get('token', None)
        except ValueError:
            token_key = None

        user = None if token_key is None else await get_user(token_key)
        if user is None:
            raise authentication_error
        scope['user'] = user

        return await self.app(scope, receive, send)
