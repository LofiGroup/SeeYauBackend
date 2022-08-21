from django.db.models import Model, CharField, ForeignKey, IntegerField, CASCADE, OneToOneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from random import randint


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    name = CharField(max_length=100)
    img_url = CharField(max_length=200)


def create_profile(user: User, name: str = "", img_url: str = ""):
    if name == "":
        name = f"User{randint(0, 10000)}"

    return Profile.objects.create(user=user, name=name, img_url=img_url)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        create_profile(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
