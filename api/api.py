from django.db.models import Q
from django_filters import rest_framework as filters
from drf_spectacular.openapi import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Song
from .serializer import SongSerializer


class SongFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name='tags', lookup_expr='icontains')
    theme = filters.CharFilter(field_name='theme', lookup_expr='icontains')
    genretype = filters.CharFilter(field_name='genretype', lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')
    creationyear = filters.CharFilter(field_name='creationyear', lookup_expr='icontains')
    composer = filters.CharFilter(field_name='composer', lookup_expr='icontains')
    fullname = filters.CharFilter(field_name='fullname', lookup_expr='icontains')

    class Meta:
        model = Song
        fields = []


@extend_schema(parameters=[OpenApiParameter(name='search', type=str, location=OpenApiParameter.QUERY,
                                            description='Поиск сразу по всем полям')], methods=["GET"])
class SongsApi(generics.ListCreateAPIView):
    """
    Эндпоинт для получения списка песен или фильтрации по различным параметрам. А также для создания новых песен.

    GET:
    Возвращает список всех песен или фильтрует их по следующим query-параметрам:
    - tags (необязательный)
    - theme (необязательный)
    - genretype (необязательный)
    - genre (необязательный)
    - author (необязательный)
    - creationyear (необязательный)
    - composer (необязательный)
    - fullname (необязательный)
    - search (необязательный): строка для поиска песен по всем полям сразу

    Примеры использования:
    GET /api/songs/
    GET /api/songs/?search=весна
    GET /api/songs/?author=Александр


    POST:
    Создаёт новую песню

    Пример использования:
    POST /api/songs/
        {
            "tags": "",
            "theme": "",
            "genretype": "6.1",
            "genre": "Романсы и песни",
            "author": "Шаховской Борис",
            "creationyear": "1961",
            "composer": "Абрамов Александр Александрович",
            "fullname": "Мы живем на севере студеном"
        }
    """

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SongFilter

    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = Song.objects.filter(
                Q(tags__icontains=search_query) |
                Q(theme__icontains=search_query) |
                Q(genretype__icontains=search_query) |
                Q(genre__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(creationyear__icontains=search_query) |
                Q(composer__icontains=search_query) |
                Q(fullname__icontains=search_query)
            )
        else:
            queryset = Song.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Метод для получения списка всех песен.

        Примеры использования: \n
        GET /api/songs/ \n
        GET /api/songs/?search=весна \n
        GET /api/songs/?author=Александр \n
        """
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Метод для создания новой песни.

        Пример использования: \n
        POST /api/songs/ \n
        { \n
            "tags": "", \n
            "theme": "", \n
            "genretype": "6.1",\n
            "genre": "Романсы и песни", \n
            "author": "Шаховской Борис", \n
            "creationyear": "1961", \n
            "composer": "Абрамов Александр Александрович", \n
            "fullname": "Мы живем на севере студеном" \n
        }
        """
        return super().post(request, *args, **kwargs)


class SongApi(generics.RetrieveDestroyAPIView):
    """
    Эндпоинт для получения песни, обновления информации о песне, удаления песни

    Позволяет получить информацию о песне по её id, обновить эту информацию, а также удалить песню

    Пример использования:
    GET /api/songs/1
    PUT /api/songs/1
    PATCH /api/songs/1
    DELETE /api/songs/1
    """

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request, *args, **kwargs):
        """
        Метод для получения информации о песне.

        Возвращает информацию о песне по её id.

        Пример использования: \n
        GET /api/songs/1
        """
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Метод для Обновления информации о песне.

        Позволяет обновить информацию о песне по её id.

        Пример использования: \n
        PUT /api/songs/1
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Метод для Частичного обновления информации о песне.

        Позволяет частично обновить информацию о песне по её id.

        Пример использования: \n
        PATCH /api/songs/1
        """
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Метод для Удаления песни.

        Позволяет удалить песню по её id.

        Пример использования: \n
        DELETE /api/songs/1
        """
        return super().delete(request, *args, **kwargs)
