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

JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", "a6a55085a15096a760daa91f0367c42be390f88a9403296c1c384a474b62a")
JWT_ACCESS_EXPIRY = os.getenv("JWT_ACCESS_EXPIRY", 60 * 24)

AUTH_ONLY_SIGNING_KEY = os.getenv("AUTH_ONLY_SIGNING_KEY", "a6a55085a15096a760daa9726h67c42be390f88a9403296c1c384ahjsb62a")
AUTH_ONLY_ACCESS_EXPIRY = os.getenv("AUTH_ONLY_ACCESS_EXPIRY", 5)

authentication_error = HttpError(status_code=401, message="Authentication error")


def decrypt_token(token: str, key: str):
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])

        data: str = payload.get("sub")
        if data is None:
            return None

        expires_in: int = payload.get("exp")
        if expires_in < datetime.utcnow().timestamp():
            return None
    except jwt.PyJWTError as e:
        print(f"Error {e}")
        return None
    return data


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        phone_number = decrypt_token(token, key=JWT_SIGNING_KEY)
        if not phone_number:
            return None
        return get_object_or_404(Profile, phone_number=phone_number)


class AuthKey(APIKeyQuery):
    param_name = "token"

    def authenticate(self, request: HttpRequest, token: str):
        return decrypt_token(token, key=AUTH_ONLY_SIGNING_KEY)


def create_token(phone_number: str):
    expires_in = current_time_in_millis() + AUTH_ONLY_ACCESS_EXPIRY
    data = {"sub": phone_number, "exp": expires_in}
    token = jwt.encode(data, JWT_SIGNING_KEY, algorithm="HS256")
    return TokenSchema(access_token=token)


def create_auth_token(phone_number: str):
    timegm(datetime.now(tz=timezone.utc).utctimetuple())
    expires_in = current_time_in_millis() + AUTH_ONLY_ACCESS_EXPIRY
    data = {"sub": phone_number, "exp": expires_in}
    token = jwt.encode(data, AUTH_ONLY_SIGNING_KEY, algorithm="HS256")
    return TokenSchema(access_token=token)
