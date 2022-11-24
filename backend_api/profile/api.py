from django.shortcuts import get_object_or_404

from ninja import Router, File, Form, UploadedFile
from typing import List, Optional

from ninja.errors import HttpError
from django.http import HttpResponse, JsonResponse

from auth.bearers import AuthBearer
from .schemas import ProfileRead, ProfileUpdate, ContactRead, LikeRead, BlackListRead
from .models.profile import Profile, get_profile_or_404

from .models.like import like, unlike, get_all_likes
from .models.contact import get_contacted_profile, contacted_with
from .models.blacklist import black_list_user, unblacklist_user, get_all_blacklists

from utils.file import save_media, delete_media
from utils.models import ErrorMessage

profile_router = Router(auth=AuthBearer())


@profile_router.get("/me", response=ProfileRead)
def get_me(request):
    profile = request.auth
    return profile


@profile_router.post("/me", auth=AuthBearer(), response=ProfileRead)
def update_profile(request, form: ProfileUpdate = Form(...), image: Optional[UploadedFile] = File(None)):
    profile: Profile = request.auth

    if form.name != "":
        profile.name = form.name

    if image is not None:
        url = save_media(profile.pk, "image/profile", image)
        delete_media(profile.img_url)
        profile.img_url = url
    profile.save()

    return profile


@profile_router.get("/contact/{user_id}", response=ContactRead)
def get_user_profile(request, user_id: int):
    query = request.auth.contacts.filter(contact__pk=user_id, is_mutual=1)
    if query.exists():
        return query.get()
    raise HttpError(status_code=404, message="No user with this id")


@profile_router.get("/contacts", response=List[ContactRead])
def get_contacts(request):
    return request.auth.contacts.filter(is_mutual=1)


@profile_router.post("/contact/{user_id}", response={200: ContactRead, 403: ErrorMessage})
def update_contact(request, user_id: int):
    profile = request.auth

    contact = contacted_with(profile, user_id)

    if contact.is_mutual == 0:
        return 403, ErrorMessage.build("This user don't know you yet")
    return 200, contact


@profile_router.post("/like/{user_id}", response=LikeRead)
def like_user(request, user_id: int):
    profile = request.auth
    user = get_contacted_profile(profile, user_id)

    return like(profile, user)


@profile_router.post("/unlike/{user_id}")
def unlike_user(request, user_id: int):
    profile = request.auth
    user = get_contacted_profile(profile, user_id)

    unlike(profile, user)
    return HttpResponse(status=204)


@profile_router.get("/likes", response=List[LikeRead])
def get_likes(request, from_date: int):
    return get_all_likes(request.auth, from_date)


@profile_router.post("/blacklist-user/{user_id}", response=BlackListRead)
def blacklist_user(request, user_id: int):
    profile = request.auth

    return black_list_user(profile, user_id)


@profile_router.post("/remove-from-blacklist/{user_id}", response=ContactRead)
def remove_from_blacklist(request, user_id: int):
    profile = request.auth

    return unblacklist_user(profile, user_id)


@profile_router.get("/get-blacklist", response=List[BlackListRead])
def get_blacklist(request, from_date: int):
    return get_all_blacklists(request.auth, from_date)

