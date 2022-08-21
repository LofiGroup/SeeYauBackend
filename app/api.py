from ninja import NinjaAPI
from auth.api import auth_router
from profile.api import profile_router
from chat.api import chat_router

api = NinjaAPI()
api.add_router("/auth", auth_router)
api.add_router("/profiles", profile_router)
api.add_router("/chat", chat_router)
