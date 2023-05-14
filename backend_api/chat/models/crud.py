from django.db.models import ObjectDoesNotExist

from chat.schemas import ChatMessageCreate
from .models import ChatRoom, ChatMessage
from profile.models.profile import Profile
from utils.utils import IS_ONLINE
from chat.firebase_messaging import sync_data


def get_chat_room(room_name):
    return ChatRoom.objects.get(pk=room_name)


def get_all_chats(user: Profile):
    return user.chats.all()


def user_in_chat(user, chat):
    return chat.users.filter(pk=user.pk).exists()


def save_chat_message(user: Profile, message: ChatMessageCreate, extra: str = "") -> ChatMessage | None:
    try:
        chat = ChatRoom.objects.get(pk=message.chat_id)
    except ObjectDoesNotExist:
        return None

    if not chat.users.filter(pk=user.pk).exists():
        return None

    message_type = message.message_type
    if message_type is None:
        message_type = "plain"

    partner: Profile = chat.users.exclude(pk=user.pk).get()
    if partner.last_seen != IS_ONLINE:
        sync_data(partner)

    return chat.messages.create(message=message.message, author=user, message_type=message_type, extra=extra)
