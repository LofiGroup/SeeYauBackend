from django.db.models import Model, CharField, ForeignKey, IntegerField, CASCADE
from django.contrib.auth.models import User

from random import randint


class Profile(Model):
    user_id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    img_url = CharField(max_length=200)


def create_profile(user_id: int, name: str = "", img_url: str = ""):
    if name == "":
        name = f"User{randint(0, 10000)}"

    return Profile.objects.create(user_id=user_id, name=name, img_url=img_url)
