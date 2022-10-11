from django.shortcuts import get_object_or_404
from django.db.models import ObjectDoesNotExist
from channels.db import database_sync_to_async

from .jwt_auth import decrypt_token, authentication_error
from utils.utils import parse_query_string
from profile.models.profile import Profile


@database_sync_to_async
def get_user(token):
    phone_number = decrypt_token(token)
    if not phone_number:
        return None
    try:
        return Profile.objects.filter(phone_number=phone_number).get()
    except ObjectDoesNotExist:
        return None


class TokenAuthMiddleWare:
    header: str = b"authorization"

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        token = self.get_token_from_header(scope)
        if not token:
            token = self.get_token_from_query(scope)

        user = None if token is None else await get_user(token)
        if user is None:
            raise authentication_error
        scope['user'] = user

        return await self.app(scope, receive, send)

    @classmethod
    def get_token_from_header(cls, scope):
        headers = dict(scope['headers'])
        auth_value = headers.get(cls.header)
        if auth_value is None:
            return None
        return auth_value.decode().split(" ")[1]

    @classmethod
    def get_token_from_query(cls, scope):
        queries = parse_query_string(scope['query_string'])
        token_key = queries.get('token', None)
        print(f"Token form query: {token_key}")
        if not token_key:
            return None
        return token_key
