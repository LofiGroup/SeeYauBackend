from ninja.security import HttpBearer
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import os
import jwt
from datetime import datetime, timedelta
from .schemas import TokenSchema

JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", "a6a55085a15096a760daa91f0367c42be390f88a9403296c1c384a474b62a")
JWT_ACCESS_EXPIRY = os.getenv("JWT_ACCESS_EXPIRY", 60 * 24)


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        try:
            payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=["HS256"])

            username: str = payload.get("sub")
            if username is None:
                return None

            expires_in: int = payload.get("exp")
            if expires_in < datetime.utcnow().timestamp():
                return None
        except jwt.PyJWTError:
            return None
        return get_object_or_404(User, username=username)


def create_token(username):
    expires_in = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_EXPIRY)
    data = {"sub": username, "exp": expires_in}
    token = jwt.encode(data, JWT_SIGNING_KEY, algorithm="HS256")
    return TokenSchema(access_token=token, expires_in=expires_in)
