from django.shortcuts import get_object_or_404

from ninja import Router, File, Form, UploadedFile
from typing import List, Optional

from ninja.errors import HttpError

from auth.jwt_auth import AuthBearer
from .schemas import ProfileRead, ProfileUpdate, ContactRead, LikeRead
from .models.profile import Profile

from utils.utils import current_time_in_millis, save_image, delete_media
from utils.models import ErrorMessage

profile_router = Router(auth=AuthBearer())


@profile_router.get("/me", response=ProfileRead)
def get_me(request):
    profile = request.auth
    return profile


@profile_router.get("/{user_id}", response=ContactRead)
def get_user_profile(request, user_id: int):
    query = request.auth.contacts.filter(contact__pk=user_id, is_mutual=1)
    if query.exists():
        return query.get()
    raise HttpError(status_code=404, message="No user with this id")


@profile_router.post("/me", auth=AuthBearer(), response=ProfileRead)
def update_profile(request, form: ProfileUpdate = Form(...), image: Optional[UploadedFile] = File(None)):
    profile: Profile = request.auth

    if form.name != "":
        profile.name = form.name

    if image is not None:
        url = save_image(profile.pk, image)
        delete_media(profile.img_url)
        profile.img_url = url
    profile.save()

    return profile


@profile_router.get("/contacts", response=List[ContactRead])
def get_contacts(request):
    return request.auth.contacts.filter(is_mutual=1)


@profile_router.post("/contact/{user_id}", response={200: ContactRead, 403: ErrorMessage, 405: ErrorMessage})
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

    if contact.is_mutual == 0:
        return 403, ErrorMessage.build("This user don't know you yet")

    return 200, contact


@profile_router.get("/likes", response=LikeRead)
def get_likes(request, from_date: int):
    profile = request.auth

    profile.likes.filter(created_in__gt=from_date)

