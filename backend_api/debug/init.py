from django.db.models.signals import post_save

from .constants import porter_number
from profile.models.profile import Profile
from .listeners import on_new_user_created


def init_debug():
    Profile.objects.update_or_create(phone_number=porter_number, name="Портье")
    post_save.connect(on_new_user_created, sender=Profile, weak=False)
