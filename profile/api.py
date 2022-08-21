from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from ninja import Router

from auth.jwt_auth import AuthBearer
from .schemas import ProfileRead, ProfileUpdate
from .models import Profile, create_profile

profile_router = Router()


@profile_router.get("/me", response=ProfileRead, auth=AuthBearer())
def get_me(request):
    user: User = request.auth
    return user.profile


@profile_router.get("/{user_id}", response=ProfileRead, auth=AuthBearer())
def get_user_profile(request, user_id: int):
    user: User = get_object_or_404(User, pk=user_id)
    return user.profile


@profile_router.put("/me", auth=AuthBearer())
def update_profile(request, payload: ProfileUpdate):
    user: User = request.auth
    profile = user.profile

    for attr, value in payload:
        setattr(profile, attr, value)
    user.save()

    return HttpResponse(status=204)
