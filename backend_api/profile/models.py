from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField
from django.contrib.auth.models import User

from random import randint
from utils.utils import current_time_in_millis


class Profile(Model):
    phone_number = CharField(max_length=100)
    name = CharField(max_length=100)
    img_url = CharField(max_length=100, default='images/profile/blank.png')
    last_seen = BigIntegerField(default=current_time_in_millis())


class Contact(Model):
    user = ForeignKey(Profile, on_delete=CASCADE, related_name='contacts')
    contact = ForeignKey(Profile, on_delete=CASCADE, related_name='+')
    last_contact = BigIntegerField(default=current_time_in_millis)

    class Meta:
        unique_together = [('user', 'contact')]


def create_profile(user: User, name: str = ""):
    if name == "":
        name = f"User{randint(0, 10000)}"

    return Profile.objects.create(user=user, name=name)
