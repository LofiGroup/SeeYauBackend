from ninja.security import HttpBearer, APIKeyQuery
from ninja.errors import HttpError
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import os
import jwt
from datetime import datetime, timedelta, timezone
from calendar import timegm
from .schemas import TokenSchema
from profile.models import Profile
from utils.utils import current_time_in_millis
from utils import time_constants as Time

JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", "a6a55085a15096a760daa91f0367c42be390f88a9403296c1c384a474b62a")
JWT_ACCESS_EXPIRY = os.getenv("JWT_ACCESS_EXPIRY", 3 * Time.month)

AUTH_ONLY_SIGNING_KEY = os.getenv("AUTH_ONLY_SIGNING_KEY", "a6a55085a15096a760daa9726h67c42be390f88a9403296c1c384ahjsb62a")
AUTH_ONLY_ACCESS_EXPIRY = os.getenv("AUTH_ONLY_ACCESS_EXPIRY", 5 * Time.minute)

authentication_error = HttpError(status_code=401, message="Authentication error")


def decrypt_token(token: str, key: str = JWT_SIGNING_KEY):
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])

        data: str = payload.get("sub")
        if data is None:
            return None

        expires_in: int = payload.get("exp")
        if expires_in < datetime.utcnow().timestamp():
            return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None
    return data


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        phone_number = decrypt_token(token)
        if not phone_number:
            return None
        return get_object_or_404(Profile, phone_number=phone_number)


class AuthKey(APIKeyQuery):
    param_name = "token"

    def authenticate(self, request: HttpRequest, token: str):
        return decrypt_token(token, key=AUTH_ONLY_SIGNING_KEY)


def create_token(phone_number: str):
    return get_new_token(phone_number, JWT_SIGNING_KEY, JWT_ACCESS_EXPIRY)


def create_auth_token(phone_number: str):
    return get_new_token(phone_number, AUTH_ONLY_SIGNING_KEY, AUTH_ONLY_ACCESS_EXPIRY)


def get_new_token(data: str, key: str, expiry: int):
    expires_in = (current_time_in_millis() + expiry) // 1000
    data = {"sub": data, "exp": expires_in}
    token = jwt.encode(data, key, algorithm="HS256")
    return TokenSchema(access_token=token)
