from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField, BooleanField
from django.shortcuts import get_object_or_404
from utils.utils import current_time_in_millis, IS_ONLINE


class Profile(Model):
    phone_number = CharField(max_length=100)
    name = CharField(max_length=100)
    img_url = CharField(max_length=100, default='images/profile/blank.png')
    last_seen = BigIntegerField(default=current_time_in_millis())


def get_profile_or_404(user_id: int):
    return Profile.objects.get_object_or_404(pk=user_id)


def create_or_update_profile(name: str, phone_number: str):
    query = Profile.objects.filter(phone_number=phone_number)
    if query.exists():
        query.update(name=name)
    else:
        Profile.objects.create(name=name, phone_number=phone_number)


def set_user_is_online(user_id: int):
    query = Profile.objects.filter(pk=user_id)
    if query.exists():
        query.update(last_seen=IS_ONLINE)


def set_user_is_offline(user_id: int):
    query = Profile.objects.filter(pk=user_id)
    if query.exists():
        query.update(last_seen=current_time_in_millis())