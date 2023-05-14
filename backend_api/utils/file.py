import os
import json
from pathlib import Path

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings

from .utils import current_time_in_millis, resolve_media_url
from .image_preview import set_image_extra, set_video_extra, set_audio_extra


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


def get_file_size(file_path: str, file_exists) -> int:
    if not file_exists:
        return 0
    return os.stat(file_path).st_size


def resolve_extra(message_type: str, media_uri: str):
    file_path = f"media/{media_uri}"

    file_exists = os.path.exists(file_path)

    extra = {
        "file_info": {
            "uri": resolve_media_url(media_uri),
            "file_size": get_file_size(file_path, file_exists)
        },
    }

    match message_type:
        case "video":
            set_video_extra(extra, file_path, file_exists)
        case "image":
            set_image_extra(extra, file_path, file_exists)
        case "audio":
            set_audio_extra(extra, file_path, file_exists)

    return json.dumps(extra)
