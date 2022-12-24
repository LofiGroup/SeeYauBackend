import os
import jwt
from datetime import datetime
from utils.utils import current_time_in_millis
from utils import time_constants as Time

JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", "a6a55085a15096a760daa91f0367c42be390f88a9403296c1c384a474b62a")
JWT_ACCESS_EXPIRY = os.getenv("JWT_ACCESS_EXPIRY", 3 * Time.month)

AUTH_ONLY_SIGNING_KEY = os.getenv("AUTH_ONLY_SIGNING_KEY", "a6a55085a15096a760daa9726h67c42be390f88a9403296c1c384ahjsb62a")
AUTH_ONLY_ACCESS_EXPIRY = os.getenv("AUTH_ONLY_ACCESS_EXPIRY", 5 * Time.minute)


def decrypt_token(token: str, key: str = JWT_SIGNING_KEY):
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])

        data: int = payload.get("sub")
        if data is None:
            return None

        expires_in: int = payload.get("exp")
        if expires_in < datetime.utcnow().timestamp():
            return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError as error:
        print(error)
        return None
    except Exception:
        return None
    return data


def create_token(data: int):
    return get_new_token(data, JWT_SIGNING_KEY, JWT_ACCESS_EXPIRY)


def create_auth_token(phone_number: str):
    return get_new_token(phone_number, AUTH_ONLY_SIGNING_KEY, AUTH_ONLY_ACCESS_EXPIRY)


def get_new_token(data: int, key: str, expiry: int):
    expires_in = (current_time_in_millis() + expiry) // 1000
    data = {"sub": data, "exp": expires_in}
    return jwt.encode(data, key, algorithm="HS256")
