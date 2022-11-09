import time
import os
from pathlib import Path

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from django.conf import settings


IS_ONLINE = 5555555555555


def current_time_in_millis():
    return time.time_ns() // 1_000_000


def parse_query_string(query):
    if query == b'':
        return dict()
    return dict((x.split('=') for x in query.decode().split("&")))


def save_image(user_id: str, file: UploadedFile):
    ext = file.name.split(".")[-1]
    file_path = f"images/profile/{user_id}_{current_time_in_millis()}.{ext}"
    return save_file(file_path, file)


def delete_media(path: str):
    if path == settings.DEFAULT_IMAGE_PATH:
        return
    path = Path(settings.MEDIA_ROOT + path)
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def save_file(file_name: str, file: UploadedFile):
    with default_storage.open(file_name, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_name


def resolve_media_url(url):
    if url == "":
        return ""

    domain = settings.DOMAIN_NAME
    media_url = settings.MEDIA_URL

    return f"https://{domain}{media_url}{url}"


def entries_in_list(elements: list, array: list) -> bool:
    for a in array:
        for elem in elements:
            if a == elem:
                return True
    return False
