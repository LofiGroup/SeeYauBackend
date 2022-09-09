from ninja import Schema, Field


class ProfileUpdate(Schema):
    name: str
    img_url: str


class ProfileRead(Schema):
    user_id: str = Field(alias="user.pk")
    name: str
    img_url: str


class ContactRead(Schema):
    id: int = Field(alias="contact.pk")
    name: str = Field(alias="contact.name")
    img_url: str = Field(alias="contact.img_url")
    last_contact: int
