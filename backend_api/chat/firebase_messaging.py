import firebase_admin.messaging as messaging
from profile.models.profile import Profile


sync_data_key = "SYNC_DATA"


def sync_data(user: Profile):
    if user.firebase_token is None:
        return

    message = messaging.Message(
        data={
            "action": "sync_data"
        },
        android=messaging.AndroidConfig(collapse_key=sync_data_key),
        token=user.firebase_token,
    )
    response = messaging.send(message)

    print(f"Sent message to firebase: {response}")
