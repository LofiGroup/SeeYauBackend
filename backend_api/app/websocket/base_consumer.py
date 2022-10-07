import json


class WebsocketError:
    def __init__(self, error_message: str):
        self.error_message: str = error_message


class Method:
    type: str

    @staticmethod
    async def process(consumer, data):
        pass


class Consumer:
    ctype: str
    methods: dict
    ERROR_RESPONSE: str = "error"

    def __init__(self):
        self.channel_name = ""
        self.channel_layer = None
        self.scope = None
        self.on_send = None

    async def connect(self, channel_name, channel_layer, scope, on_send):
        self.channel_name = channel_name
        self.channel_layer = channel_layer
        self.scope = scope
        self.on_send = on_send

        await self.on_connect()

    async def on_connect(self):
        pass

    async def disconnect(self):
        await self.on_disconnect()

        self.channel_name = ""
        self.channel_layer = None
        self.scope = None
        self.on_send = None

    async def on_disconnect(self):
        pass

    async def on_receive_message(self, data: dict):
        request_type = data['type']
        method = self.methods[request_type]
        if method is None:
            await self.send_error_response(f"Unknown method type: {request_type}")
            return
        await method.process(self, data)

    async def send_to_group(self, group_name, data):
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "send_response",
                "ctype": self.ctype,
                "data": data
            }
        )

    async def send(self, data: dict):
        await self.on_send(text_data=json.dumps({
            'type': self.ctype,
            'data': data
        }))

    async def send_error_response(self, message):
        await self.send({
            'type': self.ERROR_RESPONSE,
            'error_message': message
        })

    async def request_is_invalid(self, result, target_class=None):
        if result is WebsocketError:
            await self.send_error_response(result.error_message)
            return True
        elif target_class is not None and not isinstance(result, target_class):
            await self.send_error_response("Unknown error while sending message")
            return True
        return False
