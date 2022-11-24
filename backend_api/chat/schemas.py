from ninja import Schema, Field

from .models.models import ChatUser
from utils.utils import resolve_media_url


class ChatMessageCreate(Schema):
    local_id: int
    message: str
    chat_id: int
    message_type: str | None


class ChatMessageRead(Schema):
    id: int
    message: str
    chat_id: int
    message_type: str
    media_uri: str | None
    created_in: int
    author: int = Field(alias="author.pk")

    @staticmethod
    def resolve_media_uri(obj):
        return resolve_media_url(obj.media_uri)


class ChatMessageCreated(Schema):
    local_id: int
    real_id: int
    created_in: int


def chats_to_chat_updates(user, chats, from_date):
    chat_updates = []

    for chat in chats:
        chat_update = chat_to_chat_update(user, chat, from_date)
        chat_updates.append(chat_update)
    return chat_updates


def chat_to_chat_update(user, chat, from_date):
    query = chat.messages.filter(updated_in__gt=from_date)
    me: ChatUser = chat.chatusers.filter(user=user).get()
    partner: ChatUser = chat.chatusers.exclude(user=user).get()

    chat_update = {
        "id": chat.pk,
        "created_in": chat.created_in,
        "new_messages": [ChatMessageRead.from_orm(message).dict() for message in query.all()],
        "partner_id": partner.user.pk,
        "last_visited": me.read_in,
        "partner_last_visited": partner.read_in,
    }
    return chat_update

