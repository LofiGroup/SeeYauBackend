from django.db.models import Model, ForeignKey, CASCADE, BigIntegerField, Q
from ninja.errors import HttpError

from .profile import Profile, get_profile_or_404
from .like import Like
from .contact import Contact, contacted_with
from utils.utils import current_time_in_millis


class BlackList(Model):
    who: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='blacklist')
    whom: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='in_blacklist')
    when: int = BigIntegerField(default=current_time_in_millis)

    class Meta:
        unique_together = [('who', 'whom')]


def black_list_user(profile: Profile, user_id: int) -> BlackList:
    query = profile.blacklist.filter(whom__pk=user_id)

    if not query.exists():
        user = get_profile_or_404(user_id)

        blacklist = profile.blacklist.create(whom=user)
        delete_all_relating_data(blacklist)
        return blacklist
    raise HttpError(status_code=409, message="User is already in blacklist")


def unblacklist_user(profile: Profile, user_id: int):
    query = profile.blacklist.filter(whom__pk=user_id)

    if query.exists():
        query.delete()
        return contacted_with(profile, user_id)
    raise HttpError(status_code=404, message="User is not in blacklist")


def get_all_blacklists(profile: Profile, from_date: int):
    return BlackList.objects.filter(Q(whom=profile) | Q(who=profile)).filter(when__gt=from_date)


def delete_all_relating_data(blacklist: BlackList):
    Contact.objects.filter(user=blacklist.who, contact=blacklist.whom).delete()

    likes_query = (Like.objects.filter(who=blacklist.who, whom=blacklist.whom) | Like.objects.filter(who=blacklist.whom, whom=blacklist.who))
    likes_query.delete()

