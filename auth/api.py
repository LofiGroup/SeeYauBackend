from ninja import Router
from ninja.errors import ValidationError, HttpError

from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from .schemas import TokenSchema, AuthorizeSchema
from .jwt_auth import AuthBearer, create_token
from profile.models import Profile, create_profile

auth_router = Router()
auth_error = HttpError(status_code=401, message="Incorrect password or email")


@auth_router.post("/login", response=TokenSchema)
def login(request: HttpRequest, data: AuthorizeSchema):
    try:
        user_model = get_user_model().objects.get(username=data.email)
    except get_user_model().DoesNotExist:
        raise auth_error

    if not check_password(data.password, user_model.password):
        raise auth_error

    return create_token(data.email)


@auth_router.post("/register", response=TokenSchema)
def register(request: HttpRequest, data: AuthorizeSchema):
    try:
        get_user_model().objects.get(username=data.email)
    except get_user_model().DoesNotExist:
        user: User = User.objects.create_user(username=data.email, password=data.password)
        create_profile(user.pk)
        return create_token(data.email)
    else:
        raise HttpError(status_code=409, message="User with same email already exists.")
