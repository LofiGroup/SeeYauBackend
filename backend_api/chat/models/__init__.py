from django.db.models.signals import post_save
from django.dispatch import receiver

from profile.models.blacklist import BlackList
from chat.models.models import ChatRoom
from app.websocket.websocket_on_event import on_event, on_send_message


response_type = "you_are_blacklisted"


@receiver(post_save, sender=BlackList)
def on_user_is_black_listed(sender, instance: BlackList, created, **kwargs):
    if instance.is_active:
        chat_query = ChatRoom.objects.filter(users__in=[instance.who], is_private=1) & ChatRoom.objects.filter(users__in=[instance.whom], is_private=1)
        chat_query.delete()

    data = {
        'type': response_type,

        'id': instance.pk,
        'user_id': instance.who.pk,
        'when': instance.when,
        'is_active': bool(instance.is_active)
    }
    on_send_message(instance.whom.pk, 'profile', data)
