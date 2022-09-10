from ninja import NinjaAPI
from auth.api import auth_router
from profile.api import profile_router
from chat.api import chat_router
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

if settings.DEBUG:
    api = NinjaAPI()
else:
    api = NinjaAPI(docs_decorator=staff_member_required)

api.add_router("/auth", auth_router)
api.add_router("/profiles", profile_router)
api.add_router("/chat", chat_router)
