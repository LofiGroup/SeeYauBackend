import time
from typing import List, Optional

from ninja import Router, File, UploadedFile
from ninja.errors import HttpError
from utils.file import save_media, delete_media

from django.http import HttpRequest, HttpResponse
from django.core.cache import cache

from .schemas import TokenSchema, VerifySchema, StartAuthSchema, VerifyResponse
from .bearers import AuthBearer, AuthKey
from .jwt_auth import create_token, create_auth_token
from profile.models.profile import Profile, create_or_update_profile, create_profile_without_phone
from utils.models import ErrorMessage

import json

auth_router = Router()


def auth(phone_number: str):
    exists = create_or_update_profile(phone_number)
    token = create_token(phone_number)

    return VerifyResponse(access_token=token, exists=exists)


def verify_request_is_valid(data: VerifySchema, verify: dict):
    return verify['code'] == data.code


@auth_router.post("/verify", response={200: VerifyResponse, 401: ErrorMessage}, auth=AuthKey())
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
        return 200, auth(json_data['phone_number'])
    return 401, ErrorMessage.build("Wrong code")


@auth_router.post("/start", response=TokenSchema)
def start(request: HttpRequest, data: StartAuthSchema):
    cached_data: str = json.dumps({
        'phone_number': data.phone_number,
        'code': "1234",
    })
    cache.set(data.phone_number, cached_data, 5 * 60000)
    return TokenSchema(access_token=create_auth_token(data.phone_number))


@auth_router.post("quick-auth", response=TokenSchema)
def quick_auth(request: HttpRequest, image: Optional[UploadedFile] = File(None)):
    profile = create_profile_without_phone()

    if image is not None:
        url = save_media(profile.pk, "image/profile", image)
        profile.img_url = url
    profile.save()

    return TokenSchema(access_token=create_token(profile.pk))


@auth_router.get("/check", auth=AuthBearer())
def check(request: HttpRequest):
    return HttpResponse(status=204)
