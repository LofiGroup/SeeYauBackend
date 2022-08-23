from django.db.models import (Model, CharField, ForeignKey, IntegerField, CASCADE,
                              OneToOneField, QuerySet, SET, ManyToManyField, DateTimeField)
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver
from random import randint
from profile.models import Profile
from chat.exceptions import already_friends_error
from datetime import datetime
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZWQiLCJleHAiOjE2NjEwNDQxNDAuOTAzMDc2fQ.0nQQBzc9_ywAKhxqG3W8_3cJI4eNpz4aqNzAe-JGqqM
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZWQiLCJleHAiOjE2NjExMjQ2MTkuOTUyMTMxfQ.RvbhLk3yDA3DTlKhj02wnlVWMiyejIPe0FvwjbChp8g


def get_sentinel_profile():
    return User.objects.get_or_create(username='deleted')[0]


class Friend(Model):
    friend: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='friends')
    friend_to: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='friends_to')

    class Meta:
        unique_together = [('friend', 'friend_to')]


class ChatRoom(Model):
    users = ManyToManyField(to=Profile, through='ChatUser', related_name='chats')


class ChatUser(Model):
    chat = ForeignKey(ChatRoom, on_delete=CASCADE)
    user = ForeignKey(Profile, on_delete=CASCADE)


class ChatMessage(Model):
    message = CharField(max_length=200)
    created_in = DateTimeField(default=datetime.utcnow)
    author = ForeignKey(Profile, on_delete=SET(get_sentinel_profile), related_name='messages')
    chat = ForeignKey(ChatRoom, on_delete=CASCADE, related_name='messages')


def get_chat_room(room_name):
    return ChatRoom.objects.get(pk=room_name)


def get_all_chats(user: Profile):
    return user.chats.all()


def user_in_chat(user, chat):
    return chat.users.filter(pk=user.pk).exists()


def get_friends(profile: Profile):
    return profile.friends.all()


def add_friend(profile: Profile, friend_to: Profile):
    if profile.pk == friend_to.pk:
        raise already_friends_error
    try:
        profile.friends.create(friend_to=friend_to)
    except IntegrityError:
        raise already_friends_error


def remove_friend(profile: Profile, friend_to: Profile):
    profile.friends.filter(friend_to=friend_to).delete()


def is_friends_with(profile: Profile, potential_friend: Profile):
    return potential_friend.friends.filter(friend_to=profile).exists()


@receiver(post_save, sender=Friend)
def check_if_mutual_friends(sender, instance: Friend, created, **kwargs):
    if created:
        if is_friends_with(instance.friend, instance.friend_to):
            chat = ChatRoom.objects.create()
            chat.users.add(instance.friend)
            chat.users.add(instance.friend_to)

