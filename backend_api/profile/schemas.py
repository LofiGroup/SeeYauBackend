from ninja import Schema, Field
from utils.utils import resolve_media_url


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

    @staticmethod
    def resolve_img_url(obj):
        return resolve_media_url(obj.contact.img_url)
