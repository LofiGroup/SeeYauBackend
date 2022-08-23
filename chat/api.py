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
from .schemas import ChatUpdates, ChatUpdateRequest

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


@chat_router.get("get-all-updated", response=List[ChatUpdates])
def get_all_updates(request, chat_update_request: ChatUpdateRequest):
    user = request.auth
    chats = user.profile.chats.all()
    from_date = chat_update_request.from_date

    chat_updates = []

    for chat in chats:
        chat_update = ChatUpdates(
            id=chat.pk,
            new_messages=chat.messages.filter(created_in__gt=from_date),
            new_users=chat.users.filter(joined_in__gt=from_date)
        )
        chat_updates.append(chat_update)
    return chat_updates
