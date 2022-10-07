class WebsocketRequest:
    CHAT_MESSAGE: str = "chat_message"
    MARK_CHAT_AS_READ: str = "mark_chat_as_read"


class WebsocketResponse:
    CHAT_MESSAGE: str = "chat_message"
    CHAT_IS_READ: str = "chat_is_read"
    USER_ONLINE_STATUS_CHANGED: str = "online_status_changed"
    NEW_CHAT_IS_CREATED: str = "new_chat_is_created"
    ERROR: str = "error"


class WebsocketError:
    def __init__(self, error_message: str):
        self.error_message: str = error_message


chat_access_error = WebsocketError(error_message=f"Chat does not exist or you don't have access to this chat.")
