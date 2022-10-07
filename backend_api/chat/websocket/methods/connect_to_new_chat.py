from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models.models import ChatRoom
from profile.models import Contact, Profile
from app.websocket.websocket_on_event import on_event
from app.websocket.base_consumer import Method


class ConnectToNewChatMethod(Method):
    type = "connect_to_new_chat"
    response_type = "new_chat_is_created"

    @staticmethod
    async def process(consumer, data: dict):
        chat_id = data['chat_id']
        room_name = f"chat_{chat_id}"

        consumer.chat_group_names.append(room_name)
        await consumer.channel_layer.group_add(room_name, consumer.channel_name)

        await consumer.send({
            "type": ConnectToNewChatMethod.response_type,
            "chat_id": chat_id
        })


def is_contacted_with(profile: Profile, contacted_with: Profile):
    return contacted_with.contacts.filter(contact=profile).exists()


@receiver(post_save, sender=Contact)
def check_if_contact_is_mutual(sender, instance: Contact, created, **kwargs):
    if created:
        if is_contacted_with(instance.user, instance.contact):
            chat = ChatRoom.objects.create()
            chat.users.add(instance.user)
            chat.users.add(instance.contact)

            data = {'type': ConnectToNewChatMethod.type, 'chat_id': chat.pk}
            on_event(instance.user, data)
            on_event(instance.contact, data)
