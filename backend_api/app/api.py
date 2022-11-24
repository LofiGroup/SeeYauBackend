from ninja import NinjaAPI
from ninja import Router
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from ninja.errors import ValidationError

from auth.api import auth_router
from profile.api import profile_router
from chat.api import chat_router
from profile.admin_api import profile_admin_router


if settings.DEBUG:
    api = NinjaAPI()
else:
    api = NinjaAPI(docs_decorator=staff_member_required)


@api.exception_handler(ValidationError)
def custom_validation_errors(request, exc):
    print(exc.errors)
    return api.create_response(request, {"detail": exc.errors}, status=422)


api.add_router("/auth", auth_router)
api.add_router("/profiles", profile_router)
api.add_router("/chat", chat_router)

admin_router = Router()

admin_router.add_router("/profiles", profile_admin_router)
api.add_router("/admin", admin_router)
