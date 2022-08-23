from django.urls import path
from .views import index, room

urlpatterns = [
    path('', room, name='room')
]
