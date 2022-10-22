from ninja import Schema, Field
from typing import List
from datetime import datetime
import json

from .models.models import ChatMessage, ChatUser


def chat_message_to_dict(message: ChatMessage):
    return {
        "id": message.pk,
        "message": message.message,
        "created_in": message.created_in,
        "author": message.author.pk,
        "chat_id": message.chat.pk
    }


def chat_to_chat_updates(user, chats, from_date):
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
        "new_messages": [chat_message_to_dict(message) for message in query.all()],
        "partner_id": partner.user.pk,
        "last_visited": me.read_in,
        "partner_last_visited": partner.read_in,
    }
    return chat_update

