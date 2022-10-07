import json

from channels.generic.websocket import AsyncWebsocketConsumer
from chat.websocket.consumer import ChatConsumer


class MainConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_room = ""
        self.consumers: dict = {
            ChatConsumer.ctype: ChatConsumer()
        }

    async def connect(self):
        print("Connecting to websocket...")
        await self.accept()
        user = self.scope['user']
        self.user_room = f"user_{user.pk}"

        await self.channel_layer.group_add(self.user_room, self.channel_name)

        for consumer in self.consumers.values():
            await consumer.connect(self.channel_name, self.channel_layer, self.scope, self.send)
        print("Successfully connected to websocket!")

    async def disconnect(self, code):
        print(f"Disconnecting from websocket... Code: {code}")
        await self.channel_layer.group_discard(self.user_room, self.channel_name)

        for consumer in self.consumers.values():
            await consumer.disconnect()

    async def receive(self, text_data=None, bytes_data=None):
        print(f"Received data: {text_data}")
        text_data_json = json.loads(text_data)
        request_type = text_data_json['type']

        await self.consumers[request_type].on_receive_message(text_data_json['data'])

    async def send_response(self, event):
        print(f"Sending through websocket: {event}")
        await self.send(text_data=json.dumps({
            'type': event['ctype'],
            'data': event['data']
        }))

    async def on_event(self, event):
        self.consumers[event['type']].on_receive_message(event['data'])

