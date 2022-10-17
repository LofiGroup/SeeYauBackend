from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField, BooleanField
from ninja.errors import HttpError

from utils.utils import current_time_in_millis
from .profile import Profile, get_profile_or_404


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
