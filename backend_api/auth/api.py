from ninja import Router
from ninja.errors import HttpError

from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from .schemas import TokenSchema, AuthorizeSchema
from .jwt_auth import AuthBearer, create_token

auth_router = Router()
authorization_error = HttpError(status_code=401, message="Incorrect password or email")


@auth_router.post("/login", response=TokenSchema)
def login(request: HttpRequest, data: AuthorizeSchema):
    try:
        user_model = get_user_model().objects.get(username=data.email)
    except get_user_model().DoesNotExist:
        raise authorization_error

    if not check_password(data.password, user_model.password):
        raise authorization_error

    return create_token(data.email)


@auth_router.post("/register", response=TokenSchema)
def register(request: HttpRequest, data: AuthorizeSchema):
    try:
        get_user_model().objects.get(username=data.email)
    except get_user_model().DoesNotExist:
        User.objects.create_user(username=data.email, password=data.password)
        return create_token(data.email)
    else:
        raise HttpError(status_code=409, message="User with the same email already exists.")


@auth_router.get("/check", auth=AuthBearer())
def check(request: HttpRequest):
    return HttpResponse(status=204)
