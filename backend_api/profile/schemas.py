from ninja import Schema, Field
from django.forms import ModelForm
from django.conf import settings
from .models import Profile


class ProfileUpdate(Schema):
    name: str


class ProfileRead(Schema):
    user_id: str = Field(alias="user.pk")
    name: str
    img_url: str


class ContactRead(Schema):
    id: int = Field(alias="contact.pk")
    name: str = Field(alias="contact.name")
    img_url: str
    last_contact: int

    @staticmethod
    def resolve_img_url(obj):
        url = obj.contact.img_url
        if url == "":
            return ""

        domain = settings.DOMAIN_NAME
        media_url = settings.MEDIA_URL

        return f"{domain}{media_url}{url}"
