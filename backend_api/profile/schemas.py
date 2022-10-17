from ninja import Schema, Field
from utils.utils import resolve_media_url
from .models.like import get_likes_count


class ProfileUpdate(Schema):
    name: str


class ProfileRead(Schema):
    user_id: str = Field(alias="pk")
    name: str
    img_url: str

    @staticmethod
    def resolve_img_url(obj):
        return resolve_media_url(obj.img_url)


class ContactRead(Schema):
    user_id: int = Field(alias="contact.pk")
    name: str = Field(alias="contact.name")
    img_url: str
    last_seen: int = Field(alias="contact.last_seen")
    last_contact: int
    likes_count: int

    @staticmethod
    def resolve_img_url(obj):
        return resolve_media_url(obj.contact.img_url)

    @staticmethod
    def resolve_likes_count(obj):
        return get_likes_count(obj.contact)


class LikeRead(Schema):
    id: int
    by_who: int = Field(alias="who.pk")
    to_whom: int = Field(alias="whom.pk")
    when: int
    is_liked: bool
