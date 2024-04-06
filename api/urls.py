from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .api import SongsApi, SongApi

urlpatterns = [
    path('songs', SongsApi.as_view()),
    path('songs/<int:pk>', SongApi.as_view()),
    path('token', obtain_auth_token),
]
