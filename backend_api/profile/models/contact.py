from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField, BooleanField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from ninja.errors import HttpError

from utils.models import ErrorMessage
from utils.utils import current_time_in_millis
from .profile import Profile, get_profile_or_404

contacted_with_himself_error = HttpError(status_code=405, message="You contacted with yourself? Really?")


class Contact(Model):
    user = ForeignKey(Profile, on_delete=CASCADE, related_name='contacts')
    contact = ForeignKey(Profile, on_delete=CASCADE, related_name='+')
    last_contact = BigIntegerField(default=current_time_in_millis)
    is_mutual = BooleanField(default=0)

    class Meta:
        unique_together = [('user', 'contact')]


def get_contacted_profile(profile: Profile, user_id: int):
    user = get_profile_or_404(user_id)

    query = profile.contacts.filter(contact=user, is_mutual=1)
    if not query.exists():
        return HttpError(status_code=404, message="User is not yet contacted with you")
    return user


def contacted_with(profile: Profile, user_id: int):
    if profile.pk == user_id:
        raise contacted_with_himself_error

    contacted_profile = get_profile_or_404(user_id)

    query = profile.contacts.filter(contact=contacted_profile)
    if query.exists():
        query.update(last_contact=current_time_in_millis())
        contact = query.get()
    else:
        contact = profile.contacts.create(contact=contacted_profile, last_contact=current_time_in_millis())

    return contact


@receiver(post_delete, sender=Contact)
def on_contact_is_deleted(sender, instance: Contact, *args, **kwargs):
    Contact.objects.filter(user=instance.contact, contact=instance.user).update(is_mutual=0)
