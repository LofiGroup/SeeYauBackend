from ninja import Router

from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.models import User

from auth.jwt_auth import AuthBearer
from .models.models import add_friend, remove_friend
from .schemas import chat_to_chat_updates
from profile.models import Profile

chat_router = Router(auth=AuthBearer())


@chat_router.post("add-friend/{user_id}")
def add_friend_route(request, user_id: int):
    user = request.auth
    another_user = get_object_or_404(Profile, pk=user_id)

    add_friend(user, another_user)
    return HttpResponse(status=204)


@chat_router.delete("remove-friend/{user_id}")
def remove_friend_route(request, user_id: int):
    user = request.auth
    another_user = get_object_or_404(Profile, pk=user_id)

    remove_friend(user, another_user)
    return HttpResponse(status=204)


@chat_router.get("get-all-updated")
def get_all_updates(request, from_date: int):
    user = request.auth
    chats = user.chats.all()

    chat_updates = chat_to_chat_updates(user, chats, from_date)

    return JsonResponse(chat_updates, safe=False)
