from ninja import Schema


class TokenSchema(Schema):
    access_token: str


class AuthorizeSchema(Schema):
    username: str
    password: str
