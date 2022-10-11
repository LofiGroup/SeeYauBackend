from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField, BooleanField

from utils.utils import current_time_in_millis
from .profile import Profile


class Contact(Model):
    user = ForeignKey(Profile, on_delete=CASCADE, related_name='contacts')
    contact = ForeignKey(Profile, on_delete=CASCADE, related_name='+')
    last_contact = BigIntegerField(default=current_time_in_millis)
    is_mutual = BooleanField(default=0)

    class Meta:
        unique_together = [('user', 'contact')]