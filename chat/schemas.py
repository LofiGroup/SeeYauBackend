from ninja import Schema, Field
from typing import List


class Message(Schema):
    message: str
    created_in: int
    author: int = Field(alias='author.pk')


class ChatBrief(Schema):
    id: int = Field(alias="pk")
    users: List[int] = Field(alias='users.user_id')


class ChatDetailed(Schema):
    id: int = Field(alias="pk")
    users: List[int] = Field(alias='users.user_id')
    messages: List[Message] = Field(alias='messages')
