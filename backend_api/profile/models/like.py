from django.db.models import Model, CharField, ForeignKey, CASCADE, OneToOneField, BigIntegerField, ImageField, BooleanField
from .profile import Profile, get_profile_or_404
from utils.utils import current_time_in_millis
from app.websocket.websocket_on_event import on_send_message
from profile.model_converters import like_to_response_model


class Like(Model):
    who: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='liked')
    whom: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='likes')
    when: int = BigIntegerField(default=current_time_in_millis)
    is_liked = BooleanField(default=1)

    class Meta:
        unique_together = [('who', 'whom')]


def like_user(profile: Profile, user: Profile):
    (like, created) = profile.liked.update_or_create(whom=user, defaults={"is_liked": 1, "when": current_time_in_millis()})
    notify_like_is_changed(like)
    return like


def remove_like(profile: Profile, user: Profile):
    query = profile.liked.filter(whom=user)
    if query.exists():
        query.update(is_liked=0, when=current_time_in_millis())
        notify_like_is_changed(query.get())
        return


def notify_like_is_changed(like: Like):
    data = like_to_response_model(like)
    data["type"] = "like_is_updated"
    on_send_message(user_id=like.whom.pk, ctype='profile', data=data)


def get_likes_count(profile: Profile) -> int:
    return profile.likes.filter(is_liked=1).count()
