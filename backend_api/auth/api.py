from ninja import Router
from ninja.errors import HttpError

from django.http import HttpRequest, HttpResponse
from django.core.cache import cache

from .schemas import TokenSchema, VerifySchema, StartAuthSchema
from .jwt_auth import AuthBearer, create_token, AuthKey, create_auth_token
from profile.models.profile import Profile, create_or_update_profile
from utils.models import ErrorMessage

import json

auth_router = Router()


def auth(name: str, phone_number: str):
    create_or_update_profile(name, phone_number)

    return create_token(phone_number)


def verify_request_is_valid(data: VerifySchema, verify: dict):
    return verify['code'] == data.code


@auth_router.post("/verify", response={200: TokenSchema, 401: ErrorMessage}, auth=AuthKey())
def verify_code(request: HttpRequest, data: VerifySchema):
    phone_number = request.auth
    if phone_number is None:
        return 401, ErrorMessage.build("Authentication error")

    cache_data = cache.get(phone_number)
    if cache_data is None:
        return 401, ErrorMessage.build("Authentication error")

    json_data = json.loads(cache_data)
    if json_data is None:
        return 401, ErrorMessage.build("Authentication error")

    if verify_request_is_valid(data, json_data):
        cache.delete(phone_number)
        return 200, auth(json_data['name'], json_data['phone_number'])
    return 401, ErrorMessage.build("Wrong code")


@auth_router.post("/start", response=TokenSchema)
def start(request: HttpRequest, data: StartAuthSchema):
    cached_data: str = json.dumps({
        'name': data.name,
        'phone_number': data.phone_number,
        'code': "1234",
    })
    cache.set(data.phone_number, cached_data, 5 * 60000)
    return create_auth_token(data.phone_number)


@auth_router.get("/check", auth=AuthBearer())
def check(request: HttpRequest):
    return HttpResponse(status=204)
