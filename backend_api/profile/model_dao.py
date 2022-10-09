from random import randint
from .models import Profile
from utils.utils import current_time_in_millis, IS_ONLINE


def create_or_update_profile(name: str, phone_number: str):
    query = Profile.objects.filter(phone_number=phone_number)
    if query.exists():
        query.update(name=name)
    else:
        Profile.objects.create(name=name, phone_number=phone_number)


def set_user_is_online(user_id: int):
    query = Profile.objects.filter(pk=user_id)
    if query.exists():
        query.update(last_seen=current_time_in_millis())


def set_user_is_offline(user_id: int):
    query = Profile.objects.filter(pk=user_id)
    if query.exists():
        query.update(last_seen=IS_ONLINE)

