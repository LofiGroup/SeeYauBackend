from ninja import Router

from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotFound

from auth.bearers import AuthBearer
from .schemas import chat_to_chat_updates, chat_to_chat_update

chat_router = Router(auth=AuthBearer())


@chat_router.get("get-all-updated")
def get_all_updates(request, from_date: int):
    user = request.auth
    chats = user.chats.all()

    chat_updates = chat_to_chat_updates(user, chats, from_date)

    return JsonResponse(chat_updates, safe=False)


@chat_router.get("get-chat-updates/{chat_id}")
def get_chat_updates(request, chat_id: int, from_date: int = 0):
    user = request.auth
    query = user.chats.filter(pk=chat_id)
    if not query.exists():
        return HttpResponseNotFound()
    chat = query.get()
    return JsonResponse(chat_to_chat_update(user, chat, from_date), safe=False)

