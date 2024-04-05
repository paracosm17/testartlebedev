from django.urls import path

from .api import SongsApi, SongApi

urlpatterns = [
    path('songs', SongsApi.as_view()),
    path('songs/<int:pk>', SongApi.as_view()),
]
