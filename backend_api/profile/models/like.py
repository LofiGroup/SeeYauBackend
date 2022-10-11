from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField, BooleanField
from .profile import Profile, get_profile_or_404
from utils.utils import current_time_in_millis


class Like(Model):
    who = ForeignKey(Profile, on_delete=CASCADE, related_name='liked')
    whom = ForeignKey(Profile, on_delete=CASCADE, related_name='likes')
    when = BigIntegerField(default=current_time_in_millis)
    is_liked = BooleanField(default=1)

    class Meta:
        unique_together = [('who', 'whom')]


def like_user(profile: Profile, user_id: int):
    query = profile.liked.filter(whom__pk=user_id)
    if query.exists():
        query.update(is_liked=1, when=current_time_in_millis())
        return

    profile.liked.create(whom=get_profile_or_404(user_id))


def remove_like(profile, user_id: int):
    query = profile.liked.filter(whom__pk=user_id)
    if profile.liked.filter(whom__pk=user_id).exists():
        query.update(is_liked=0, when=current_time_in_millis())
        return
