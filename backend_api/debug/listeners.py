from profile.models.contact import contacted_with

from profile.models.profile import Profile
from .constants import porter_number


def on_new_user_created(sender, instance: Profile, created, **kwargs):
    if created:
        porter = Profile.objects.get(phone_number=porter_number)
        contacted_with(instance, porter.pk)
        contacted_with(porter, instance.pk)
