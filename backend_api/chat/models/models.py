from django.db.models import (Model, CharField, ForeignKey, CASCADE,
                              SET, ManyToManyField, BigIntegerField)
from django.contrib.auth.models import User

from profile.models import Profile
from datetime import datetime
from utils.utils import current_time_in_millis
from profile.models import Contact
from chat.consumer_api import notify_new_chat_is_created


def get_sentinel_profile():
    return User.objects.get_or_create(username='deleted')[0]


def get_current_time():
    return datetime.utcnow().timestamp()


class Friend(Model):
    friend: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='friends')
    friend_to: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='friends_to')

    class Meta:
        unique_together = [('friend', 'friend_to')]


class ChatRoom(Model):
    users = ManyToManyField(to=Profile, through='ChatUser', related_name='chats')


class ChatUser(Model):
    chat = ForeignKey(ChatRoom, on_delete=CASCADE, related_name="chatusers")
    user = ForeignKey(Profile, on_delete=SET(get_sentinel_profile))
    joined_in = BigIntegerField(default=current_time_in_millis)
    read_in = BigIntegerField(default=current_time_in_millis)


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

