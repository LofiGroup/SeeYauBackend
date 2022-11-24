from typing import Optional

from ninja import Router, File, Form, UploadedFile
from ninja.errors import HttpError
from django.http import JsonResponse, HttpResponseNotFound, Http404
from auth.bearers import AuthBearer
from .schemas import chats_to_chat_updates, chat_to_chat_update, ChatMessageCreate, ChatMessageRead, ChatMessageCreated
from app.websocket.websocket_on_event import on_event
from utils.file import save_media
from .websocket.methods.notify_chat_group import NotifyChatGroupMethod
from .models.crud import save_chat_message

chat_router = Router(auth=AuthBearer())


@chat_router.get("get-all-updated")
def get_all_updates(request, from_date: int):
    user = request.auth
    chats = user.chats.all()

    chat_updates = chats_to_chat_updates(user, chats, from_date)

    return JsonResponse(chat_updates, safe=False)


@chat_router.get("get-chat-updates/{chat_id}")
def get_chat_updates(request, chat_id: int, from_date: int = 0):
    user = request.auth
    query = user.chats.filter(pk=chat_id)
    if not query.exists():
        return HttpResponseNotFound()
    chat = query.get()
    return JsonResponse(chat_to_chat_update(user, chat, from_date), safe=False)


@chat_router.post("send-chat-media", response=ChatMessageCreated)
def send_chat_media(request, message_create: ChatMessageCreate = Form(...), media: Optional[UploadedFile] = File(None)):
    user = request.auth

    if media is None:
        media_uri = None
        print("Media is null")
    else:
        media_uri = save_media(file_prefix=user.pk, directory=message_create.message_type, file=media)

    message = save_chat_message(user, message_create, media_uri)
    if message is None:
        raise Http404()

    data = ChatMessageRead.from_orm(message).dict()
    data['type'] = NotifyChatGroupMethod.type
    on_event(
        user_id=user.pk,
        ctype="chat",
        data=data
    )

    return {
        "local_id": message_create.local_id,
        "real_id": message.pk,
        "created_in": message.created_in
    }
