from ninja import Schema


class TokenSchema(Schema):
    access_token: str
    expires_in: int


class AuthorizeSchema(Schema):
    email: str
    password: str
