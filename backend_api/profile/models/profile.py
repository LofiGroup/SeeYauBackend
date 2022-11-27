from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField, BooleanField
from django.shortcuts import get_object_or_404
from utils.utils import current_time_in_millis, IS_ONLINE

from random import randint


class Profile(Model):
    phone_number = CharField(max_length=100)
    name = CharField(max_length=100)
    img_url = CharField(max_length=100, default='image/profile/blank.png')
    last_seen = BigIntegerField(default=current_time_in_millis)


def get_profile_or_404(user_id: int):
    return get_object_or_404(Profile, pk=user_id)


# true if already exists
def create_or_update_profile(phone_number: str, name: str = "") -> bool:
    query = Profile.objects.filter(phone_number=phone_number)
    if query.exists():
        return True
    else:
        if name == "":
            name = f"User{randint(0, 1000000)}"
        Profile.objects.create(name=name, phone_number=phone_number)
        return False


def set_user_is_online(user_id: int):
    query = Profile.objects.filter(pk=user_id)
    if query.exists():
        query.update(last_seen=IS_ONLINE)


def set_user_is_offline(user_id: int):
    query = Profile.objects.filter(pk=user_id)
    if query.exists():
        query.update(last_seen=current_time_in_millis())