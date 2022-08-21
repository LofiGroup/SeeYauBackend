from ninja import Router
from ninja.errors import ValidationError, HttpError

from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from auth.jwt_auth import AuthBearer

from .models.models import add_friend, remove_friend

chat_router = Router()


@chat_router.post("add-friend", auth=AuthBearer())
def add_friend_route(request, user_id: int):
    user = request.auth
    another_user = get_object_or_404(User, pk=user_id)

    add_friend(user.profile, another_user.profile)
    return HttpResponse(status=204)


@chat_router.delete("remove-friend", auth=AuthBearer())
def remove_friend_route(request, user_id: int):
    user = request.auth
    another_user = get_object_or_404(User, pk=user_id)

    remove_friend(user.profile, another_user.profile)
    return HttpResponse(status=204)
