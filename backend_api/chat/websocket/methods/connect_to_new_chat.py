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


@receiver(post_save, sender=Contact)
def check_if_contact_is_mutual(sender, instance: Contact, created, **kwargs):
    if created:
        other_contact = Contact.objects.filter(user=instance.contact, contact=instance.user)
        if other_contact.exists():
            instance.is_mutual = 1
            instance.save()
            other_contact.update(is_mutual=1)

            chat = ChatRoom.objects.create()
            chat.users.add(instance.user)
            chat.users.add(instance.contact)

            data = {
                'type': ConnectToNewChatMethod.response_type,
                'chat_id': chat.pk
            }
            on_event(instance.user.pk, 'chat', data)
            on_event(instance.contact.pk, 'chat', data)
