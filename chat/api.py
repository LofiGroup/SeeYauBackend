from typing import List

from ninja import Router
from ninja.errors import ValidationError, HttpError

from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from auth.jwt_auth import AuthBearer
from .models.models import add_friend, remove_friend, get_chat_room
from .schemas import ChatBrief, ChatDetailed

chat_router = Router(auth=AuthBearer())


@chat_router.post("add-friend/{user_id}")
def add_friend_route(request, user_id: int):
    user = request.auth
    another_user = get_object_or_404(User, pk=user_id)

    add_friend(user.profile, another_user.profile)
    return HttpResponse(status=204)


@chat_router.delete("remove-friend/{user_id}")
def remove_friend_route(request, user_id: int):
    user = request.auth
    another_user = get_object_or_404(User, pk=user_id)

    remove_friend(user.profile, another_user.profile)
    return HttpResponse(status=204)


@chat_router.get("get-all", response=List[ChatBrief])
def get_all_chats(request):
    user = request.auth
    return user.profile.chats.all()


@chat_router.get("get-by-id/{chat_id}", response=ChatDetailed)
def get_chat_by_id(request, chat_id: int):
    return get_chat_room(chat_id)

