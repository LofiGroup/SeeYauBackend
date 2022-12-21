import os
import json
from pathlib import Path

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings

from .utils import current_time_in_millis, resolve_media_url


def save_media(file_prefix: str, directory: str, file: UploadedFile):
    ext = file.name.split(".")[-1]

    file_path = f"{directory}/{file_prefix}_{current_time_in_millis()}.{ext}"
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


def get_file_name_from_path(file_name: str) -> str:
    split = file_name.split("/")
    return split[-1]


def resolve_extra(message_type: str, media_uri: str):
    extra = {"uri": resolve_media_url(media_uri)}

    if message_type == "video":
        extra["thumbnail_uri"] = ""

    return json.dumps(extra)
