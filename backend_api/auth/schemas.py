from ninja import Schema


class TokenSchema(Schema):
    access_token: str


class StartAuthSchema(Schema):
    name: str
    phone_number: str


class VerifySchema(Schema):
    code: str
