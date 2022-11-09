from django.db.models.signals import post_save

from .constants import porter_number
from profile.models.profile import create_or_update_profile, Profile
from .listeners import on_new_user_created


def init_debug():
    create_or_update_profile(phone_number=porter_number, name="Портье")
    post_save.connect(on_new_user_created, sender=Profile)
