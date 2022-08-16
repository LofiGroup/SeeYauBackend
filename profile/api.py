from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, Http404

from ninja import Router

from auth.jwt_auth import AuthBearer
from .schemas import ProfileRead, ProfileUpdate
from .models import Profile, create_profile

profile_router = Router()


@profile_router.get("/me", response=ProfileRead, auth=AuthBearer())
def get_me(request):
    user: User = request.auth
    return get_object_or_404(Profile, user_id=user.pk)


@profile_router.get("/{user_id}", response=ProfileRead, auth=AuthBearer())
def get_user_profile(request, user_id: int):
    return get_object_or_404(Profile, user_id=user_id)


@profile_router.put("/me", auth=AuthBearer())
def update_profile(request, payload: ProfileUpdate):
    user: User = request.auth

    try:
        profile = get_object_or_404(Profile, user_id=user.pk)
        for attr, value in payload:
            setattr(profile, attr, value)
        profile.save()
    except Http404:
        create_profile(user_id=user.pk, name=payload.name, img_url=payload.img_url)

    return HttpResponse(status=204)
