from django.db.models import Model, ForeignKey, CASCADE, BigIntegerField, Q, BooleanField
from ninja.errors import HttpError

from .profile import Profile, get_profile_or_404
from .like import Like
from .contact import Contact, contacted_with
from utils.utils import current_time_in_millis


class BlackList(Model):
    who: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='blacklist')
    whom: Profile = ForeignKey(Profile, on_delete=CASCADE, related_name='in_blacklist')
    when: int = BigIntegerField(default=current_time_in_millis)
    is_active: bool = BooleanField(default=1)

    class Meta:
        unique_together = [('who', 'whom')]


def black_list_user(profile: Profile, user_id: int) -> BlackList:
    query = profile.blacklist.filter(whom__pk=user_id)

    user = get_profile_or_404(user_id)

    if query.exists():
        blacklist = query.get()
        if blacklist.is_active:
            raise HttpError(status_code=409, message="User is already in blacklist")

        blacklist.is_active = 1
        blacklist.save()
    else:
        blacklist = profile.blacklist.create(whom=user)
    delete_all_relating_data(blacklist)
    return blacklist


def unblacklist_user(profile: Profile, user_id: int):
    query = profile.blacklist.filter(whom__pk=user_id, is_active=1)

    if query.exists():
        blacklist = query.get()
        blacklist.is_active = 0
        blacklist.save()
        return contacted_with(profile, user_id)
    raise HttpError(status_code=404, message="User is not in blacklist")


def get_all_blacklists(profile: Profile, from_date: int):
    return BlackList.objects.filter(Q(whom=profile) | Q(who=profile)).filter(when__gt=from_date)


def delete_all_relating_data(blacklist: BlackList):
    Contact.objects.filter(user=blacklist.who, contact=blacklist.whom).delete()

    likes_query = (Like.objects.filter(who=blacklist.who, whom=blacklist.whom) | Like.objects.filter(who=blacklist.whom, whom=blacklist.who))
    likes_query.delete()

