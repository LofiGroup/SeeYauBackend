from django.db.models.signals import post_save

from profile.models.contact import contacted_with
from .constants import porter_number

from profile.models.profile import Profile
from .constants import porter_number


def on_user_is_black_listed(sender, instance: Profile, created, **kwargs):
    if created:
        porter = Profile.objects.get(phone_number=porter_number)
        contacted_with(instance, porter.pk)
        contacted_with(porter, instance.pk)


def init_debug():
    Profile.objects.update_or_create(phone_number=porter_number, name="Портье")

    post_save.connect(on_user_is_black_listed, sender=Profile, weak=False)

