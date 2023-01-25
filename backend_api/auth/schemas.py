from ninja import Schema


class TokenSchema(Schema):
    access_token: str


class VerifyResponse(Schema):
    access_token: str
    exists: bool


class StartAuthSchema(Schema):
    phone_number: str


class VerifySchema(Schema):
    code: str


class FirebaseTokenSchema(Schema):
    token: str
