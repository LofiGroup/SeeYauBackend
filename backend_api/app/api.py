from ninja import NinjaAPI
from ninja import Router
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from auth.api import auth_router
from profile.api import profile_router
from chat.api import chat_router
from debug import init_debug


from profile.admin_api import profile_admin_router

if settings.DEBUG:
    api = NinjaAPI()
else:
    api = NinjaAPI(docs_decorator=staff_member_required)

api.add_router("/auth", auth_router)
api.add_router("/profiles", profile_router)
api.add_router("/chat", chat_router)

admin_router = Router()

admin_router.add_router("/profiles", profile_admin_router)
api.add_router("/admin", admin_router)

if not settings.IS_PRODUCTION_VERSION:
    init_debug()
