from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse

from ninja import Router
from typing import List

from auth.jwt_auth import AuthBearer
from .schemas import ProfileRead, ProfileUpdate, ContactRead
from .models import Profile

from utils.utils import current_time_in_millis

profile_router = Router()


@profile_router.get("/me", response=ProfileRead, auth=AuthBearer())
def get_me(request):
    user: User = request.auth
    return user.profile


@profile_router.put("/me", auth=AuthBearer())
def update_profile(request, payload: ProfileUpdate):
    user: User = request.auth
    profile = user.profile

    for attr, value in payload:
        setattr(profile, attr, value)
    user.save()

    return HttpResponse(status=204)


@profile_router.get("/contacts", auth=AuthBearer(), response=List[ContactRead])
def get_contacts(request):
    return request.auth.profile.contacts


@profile_router.post("/contact/{user_id}", auth=AuthBearer(), response=ContactRead)
def update_contact(request, user_id: int):
    profile = request.auth.profile
    contacted_profile = get_object_or_404(Profile, pk=user_id)
    (contact, _) = profile.contacts.update_or_create(contact=contacted_profile, last_contact=current_time_in_millis())

    return contact


@profile_router.get("/{user_id}", response=ProfileRead, auth=AuthBearer())
def get_user_profile(request, user_id: int):
    user: User = get_object_or_404(User, pk=user_id)
    return user.profile
