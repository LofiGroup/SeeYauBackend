from ninja.security import HttpBearer, APIKeyQuery
from ninja.errors import HttpError
from django.http import HttpRequest

import os

ADMIN_ACCESS_KEY = os.getenv("ADMIN_ACCESS_KEY", "jretry")

authentication_error = HttpError(status_code=401, message="Authentication error")


class AdminAuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        if token != ADMIN_ACCESS_KEY:
            raise authentication_error
        return 200
