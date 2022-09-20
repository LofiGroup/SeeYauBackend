from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse

from ninja import Router, File, Form, UploadedFile
from typing import List, Optional

from ninja.errors import HttpError

from auth.jwt_auth import AuthBearer
from .schemas import ProfileRead, ProfileUpdate, ContactRead
from .models import Profile

from utils.utils import current_time_in_millis, save_image
from utils.models import ErrorMessage

profile_router = Router()


@profile_router.get("/me", response=ProfileRead, auth=AuthBearer())
def get_me(request):
    profile = request.auth
    return profile


@profile_router.post("/me", auth=AuthBearer(), response=ProfileRead)
def update_profile(request, form: ProfileUpdate = Form(...), image: Optional[UploadedFile] = File(None)):
    profile: Profile = request.auth

    for attr, value in form:
        setattr(profile, attr, value)

    if image is not None:
        url = save_image(profile.pk, image)
        profile.img_url = url
    profile.save()

    return profile


@profile_router.get("/contacts", auth=AuthBearer(), response=List[ContactRead])
def get_contacts(request):
    return request.auth.contacts


@profile_router.post("/contact/{user_id}", auth=AuthBearer(), response={200: ContactRead, 405: ErrorMessage})
def update_contact(request, user_id: int):
    profile = request.auth

    if profile.pk == user_id:
        return 405, ErrorMessage.build("You contacted with yourself? Really?")

    contacted_profile = get_object_or_404(Profile, pk=user_id)

    query = profile.contacts.filter(contact=contacted_profile)
    if query.exists():
        query.update(last_contact=current_time_in_millis())
        contact = query.get()
    else:
        contact = profile.contacts.create(contact=contacted_profile, last_contact=current_time_in_millis())

    return 200, contact


@profile_router.get("/{user_id}", response=ProfileRead, auth=AuthBearer())
def get_user_profile(request, user_id: int):
    return get_object_or_404(Profile, pk=user_id)
