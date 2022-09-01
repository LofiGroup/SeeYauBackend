from ninja import Schema, Field
from typing import List
from datetime import datetime


class Message(Schema):
    message: str
    created_in: int
    author: int = Field(alias='author.pk')


class UserBrief(Schema):
    user_id: int


class ChatUpdates(Schema):
    id: int = Field(alias="pk")
    new_users: List[UserBrief] = Field(alias='users')
    new_messages: List[Message] = Field(alias='messages')


class ChatUpdateRequest(Schema):
    from_date: int


def chat_message_to_dict(message):
    return {
        "id": message.pk,
        "message": message.message,
        "created_in": message.created_in,
        "author": message.author.pk
    }


def chat_to_chat_updates(user, chats, from_date):
    chat_updates = []

    for chat in chats:
        query = chat.messages.filter(created_in__gt=from_date)
        if not query.exists():
            continue

        chat_update = {
            "id": chat.pk,
            "new_messages": [chat_message_to_dict(message) for message in query.all()],
            "partner": chat.chatusers.exclude(id=user.pk).get().pk
        }
        chat_updates.append(chat_update)
    return chat_updates
