from ninja import Schema, Field
from typing import List
from datetime import datetime
import json

from .models.models import ChatMessage, ChatUser


class Message(Schema):
    message: str
    created_in: int
    author: int = Field(alias='author.pk')


class UserBrief(Schema):
    user_id: int


class ChatUpdateRequest(Schema):
    from_date: int


def chat_message_to_dict(message: ChatMessage):
    return {
        "id": message.pk,
        "message": message.message,
        "created_in": message.created_in,
        "author": message.author.pk,
        "chat_id": message.chat.pk
    }


def chat_message_to_json(message):
    return json.dumps(chat_message_to_dict(message))


def chat_to_chat_updates(user, chats, from_date):
    chat_updates = []

    for chat in chats:
        query = chat.messages.filter(updated_in__gt=from_date)
        me: ChatUser = chat.chatusers.filter(user=user).get()
        partner: ChatUser = chat.chatusers.exclude(user=user).get()

        chat_update = {
            "id": chat.pk,
            "new_messages": [chat_message_to_dict(message) for message in query.all()],
            "partner_id": partner.pk,
            "last_visited": me.read_in,
            "partner_last_visited": partner.read_in
        }
        chat_updates.append(chat_update)
    return chat_updates
