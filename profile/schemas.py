from ninja import Schema


class ProfileUpdate(Schema):
    name: str
    img_url: str


class ProfileRead(Schema):
    user_id: str
    name: str
    img_url: str
