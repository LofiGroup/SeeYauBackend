from django.db.models import ObjectDoesNotExist

from chat.schemas import ChatMessageCreate
from .models import ChatRoom, ChatMessage
from profile.models.profile import Profile


def get_chat_room(room_name):
    return ChatRoom.objects.get(pk=room_name)


def get_all_chats(user: Profile):
    return user.chats.all()


def user_in_chat(user, chat):
    return chat.users.filter(pk=user.pk).exists()


def save_chat_message(user: Profile, message: ChatMessageCreate, media_uri: str = None) -> ChatMessage | None:
    try:
        chat = ChatRoom.objects.get(pk=message.chat_id)
    except ObjectDoesNotExist:
        return None

    if not chat.users.filter(pk=user.pk).exists():
        return None

    message_type = message.message_type
    if message_type is None:
        message_type = "plain"

    return chat.messages.create(message=message.message, author=user, message_type=message_type, media_uri=media_uri)