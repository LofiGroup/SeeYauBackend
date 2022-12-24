from ninja.security import HttpBearer, APIKeyQuery
from ninja.errors import HttpError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from profile.models.profile import Profile
from .jwt_auth import decrypt_token, AUTH_ONLY_SIGNING_KEY

authentication_error = HttpError(status_code=401, message="Authentication error")


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        pk = decrypt_token(token)
        if not pk:
            raise authentication_error
        elif not isinstance(pk, int):
            raise authentication_error
        try:
            return get_object_or_404(Profile, pk=pk)
        except HttpError:
            raise authentication_error


class AuthKey(APIKeyQuery):
    param_name = "token"

    def authenticate(self, request: HttpRequest, token: str):
        return decrypt_token(token, key=AUTH_ONLY_SIGNING_KEY)
