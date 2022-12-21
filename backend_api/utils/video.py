from moviepy.editor import VideoFileClip
from utils.utils import resolve_media_url


def create_thumbnail(video_file_name: str) -> str:
    clip = VideoFileClip(f"media/video/{video_file_name}")

    name_without_ext = video_file_name.split(".")[0]
    path = f"video/thumbnails/{name_without_ext}.png"
    clip.save_frame(f"media/{path}", t=0.00)
    clip.close()
    return resolve_media_url(path)
