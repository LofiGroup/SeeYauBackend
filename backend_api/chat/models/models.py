from django.db.models import (Model, CharField, ForeignKey, CASCADE,
                              SET, ManyToManyField, BigIntegerField, BooleanField)
from django.contrib.auth.models import User

from profile.models.profile import Profile
from datetime import datetime
from utils.utils import current_time_in_millis


def get_sentinel_profile():
    return Profile.objects.get_or_create(phone_number='deleted', name='deleted')


def get_current_time():
    return datetime.utcnow().timestamp()


class ChatRoom(Model):
    users = ManyToManyField(to=Profile, through='ChatUser', related_name='chats')
    is_private = BooleanField(default=1)


class ChatUser(Model):
    chat = ForeignKey(ChatRoom, on_delete=CASCADE, related_name="chatusers")
    user = ForeignKey(Profile, on_delete=SET(get_sentinel_profile))
    joined_in = BigIntegerField(default=current_time_in_millis)
    read_in = BigIntegerField(default=current_time_in_millis)

    class Meta:
        unique_together = [('chat', 'user')]


class ChatMessage(Model):
    message = CharField(max_length=2000)
    created_in = BigIntegerField(default=current_time_in_millis)
    updated_in = BigIntegerField(default=current_time_in_millis)
    author = ForeignKey(Profile, on_delete=SET(get_sentinel_profile), related_name='messages')
    chat = ForeignKey(ChatRoom, on_delete=CASCADE, related_name='messages')


def get_chat_room(room_name):
    return ChatRoom.objects.get(pk=room_name)


def get_all_chats(user: Profile):
    return user.chats.all()


def user_in_chat(user, chat):
    return chat.users.filter(pk=user.pk).exists()

