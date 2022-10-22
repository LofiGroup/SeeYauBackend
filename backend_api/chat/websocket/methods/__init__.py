from chat.websocket.methods.connect_to_new_chat import ConnectToNewChatMethod
from .message_received import MessageReceivedMethod
from .mark_chat_as_read import MarkChatAsReadMethod
from .notify_online_status_changed import NotifyUserOnlineStatusChangedMethod, OnlineStatus


methods = {
    ConnectToNewChatMethod.type: ConnectToNewChatMethod,
    MessageReceivedMethod.type: MessageReceivedMethod,
    MarkChatAsReadMethod.type: MarkChatAsReadMethod,
    NotifyUserOnlineStatusChangedMethod.type: NotifyUserOnlineStatusChangedMethod,
}
