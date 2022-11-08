from websocket import WebSocketApp, enableTrace
import json
from random import randint
import os
import time

from debug.constants import porter_number
from auth.jwt_auth import create_token

port = os.getenv("PORT", "8000")

messages = ["Хммм...", "\U0001F606", "\U0001F923", "\U0001f600", "Ок"]


def on_message(websocket, msg: str):
    data_json = json.loads(msg)

    type = data_json['type']
    data = data_json['data']

    if type == "chat" and data['type'] == "new_message":
        time.sleep(3)
        websocket.send(json.dumps({
            "type": "chat",
            "data": {
                "type": "chat_message",
                "local_id": 0,
                "chat_id": data['chat_id'],
                "message": messages[randint(0, len(messages) - 1)]
            }
        }))


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_error, close_msg):
    print("Porter is out of service")


def on_open(ws):
    print("Porter is on the service")


def porter_client():
    print("Running porter...")
    token = create_token(porter_number)
    uri = f"ws://localhost:{port}/ws/main?token={token}"
    print(f"Url is {uri}")
    ws = WebSocketApp(
        uri,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever(reconnect=10)


if __name__ == '__main__':
    porter_client()
