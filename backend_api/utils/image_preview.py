from PIL.Image import open, Image
import base64
from io import BytesIO
import math
import av

fake_preview = {
    "base64": "",
    "width": 1,
    "height": 1
}


def resolve_scaled_size(size, target_size: int):
    width, height = size

    if width > height:
        return math.ceil(target_size * (float(width) / height)), target_size
    else:
        return target_size, math.ceil(target_size * (float(height) / width))


def create_base64_image_preview(image: Image) -> str:
    new_size = resolve_scaled_size(image.size, target_size=20)
    new_image = image.resize(new_size)

    buf = BytesIO()

    new_image.save(buf, "webp")
    result = base64.b64encode(buf.getvalue())

    buf.close()
    return result.decode("utf-8")


def set_preview_extra(extra: dict, image: Image):
    extra["preview"] = {
        "base64": create_base64_image_preview(image),
        "width": image.width,
        "height": image.height
    }


def set_image_extra(extra: dict, path: str, file_exists):
    if not file_exists:
        extra["preview"] = fake_preview
        return

    with open(path) as image:
        set_preview_extra(extra, image)


def set_video_extra(extra: dict, path: str, file_exists):
    if not file_exists:
        extra["preview"] = fake_preview
        extra["duration"] = 0
        return

    try:
        with av.open(path) as container:
            stream = container.streams.video[0]
            extra["duration"] = int(container.duration / 1000)

            frames = container.decode(stream)

            if stream.frames == 0:
                extra["preview"] = fake_preview

            else:
                frame = next(frames)

                image = frame.to_image()
                set_preview_extra(extra, image)
                image.close()
    except Exception:
        extra["duration"] = 0
        extra["preview"] = fake_preview


def set_audio_extra(extra: dict, path: str, file_exists):
    if not file_exists:
        extra["duration"] = 0
        return

    with av.open(path) as container:
        extra["duration"] = int(container.duration / 1000)
