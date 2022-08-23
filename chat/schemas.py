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
