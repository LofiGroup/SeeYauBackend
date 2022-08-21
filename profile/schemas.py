from ninja import Schema, Field


class ProfileUpdate(Schema):
    name: str
    img_url: str


class ProfileRead(Schema):
    user_id: str = Field(alias="user.pk")
    name: str
    img_url: str
