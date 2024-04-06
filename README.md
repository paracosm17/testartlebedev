# Тестовое задание. Создание API на основе готовых данных
- [x] Взять любую таблицу длиной более 100 строк из реестра открытых данных Минкульта России
https://opendata.mkrf.ru/opendata.
- [x] Написать парсер на Python, который сохранит данные из таблицы в базу данных.
- [x] Реализовать на Django API для доступа к базе данных.
- [x] Реализовать поиск по данным через API.
- [x] Создать Docker-образ, который парсит встроенную в него таблицу и поднимает сервер с 
базой данных и API.
- [x] Написать документацию к API.

## Документация к проекту

### Установка

#### Образ из докерхаба: <br>
```bash
sudo docker run -p 5439:5432 -p 8000:8000 -d -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb paracosm17/testartlebedev
```

#### Из исходников: <br>
```bash
git clone git@github.com:paracosm17/testartlebedev.git
cd testartlebedev
sudo docker build -t testartlebedev .
sudo docker run -p 5439:5432 -p 8000:8000 -d -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb testartlebedev
```

#### Важно!
Порты `5439` и `8000` должны быть свободны на целевой машине. В случае, если они заняты, замените их. Например, на `5438` или `8001` (порт который перед : )

#### Проверка
С помощью curl быстро проверим, что сервис успешно запустился и апи возвращает код `200`
```bash
curl -o /dev/null -I -L -s -w "%{http_code}\n" http://127.0.0.1:8000/api/songs
```
output:
```bash
200
```

### Особенности
   - БД `PostgreSQL`
   - Для данных используется таблица патриотической музыки 
https://opendata.mkrf.ru/opendata/7705851331-patriot_music
   - Встроенная в проект таблица укорочена до 300 строк для экономии времени
   - Поддерживаемые форматы данных: `json`, `csv`
   - Возможность подгрузить данные из таблицы в БД с помощью команды <br>
   ``python manage.py parsetable songs.json`` <br>
   Команда проверит, есть ли уже записи в базе данных, если нет, то подгрузит. Если записи уже есть, то не станет и 
предупредит, что данные уже загружены. <br>
   Также предусмотрен флаг `--force` для того чтобы в любом случае подгрузить данные, несмотря на то, есть ли уже 
   что-то в бд или нет <br>
   ``python manage.py parsetable songs.csv --force``
   - Реализовано API с помощью `djangorestframework`
   - Реализован поиск по полям с помощью `django-filter`
   - Реализован поиск сразу по всем полям с помощью query-параметра `search`
   - Докеризирован
   - Реализована документация к API в виде `Swagger UI` с помощью библиотеки `drf-spectacular`
   - RESTful
   - Swagger UI находится по адресу http://127.0.0.1:8000/api/docs/
   - Каждый метод и эндпоинт документирован с помощью docstring. Оно автоматически показывается в Swagger

[![image.png](https://i.postimg.cc/4xN99yff/image.png)](https://postimg.cc/56TycxQT)
[![image.png](https://i.postimg.cc/W3HvX9rY/image.png)](https://postimg.cc/ftmpbf8Y)
[![image.png](https://i.postimg.cc/s21y7dGG/image.png)](https://postimg.cc/yJqwCGP7)

## Документация к API

### Оглавление
1. [Обзор API](#обзор-api)
2. [Эндпоинты](#эндпоинты)
   - [Получение списка песен](#получение-списка-песен)
   - [Создание новой песни](#создание-новой-песни)
   - [Получение информации о песне](#получение-информации-о-песне)
   - [Обновление информации о песне](#обновление-информации-о-песне)
   - [Удаление песни](#удаление-песни)
3. [Примеры](#примеры)

## Обзор API

API патриотической музыки предоставляет доступ к базе данных песен, включая их теги, тематики, жанры и другие 
характеристики. Этот API позволяет получать список песен, создавать новые записи, обновлять и удалять существующие.

### Базовый URL

```
http://127.0.0.1:8000/api/songs/
```

### Swagger UI (документация)

```
http://127.0.0.1:8000/api/docs/
```

## Эндпоинты

### Получение списка песен

- **URL**: `/api/songs/`
- **Метод**: `GET`
- **Описание**: Возвращает список всех песен с возможностью фильтрации по различным параметрам.
- **Параметры**:
  - `tags`: фильтр по тегам
  - `theme`: фильтр по теме
  - `genretype`: фильтр по типу жанра
  - `genre`: фильтр по жанру
  - `author`: фильтр по автору
  - `creationyear`: фильтр по году создания
  - `composer`: фильтр по композитору
  - `fullname`: фильтр по полному названию
  - `search`: поиск по всем полям сразу

### Создание новой песни

- **URL**: `/api/songs/`
- **Метод**: `POST`
- **Описание**: Создаёт новую песню с указанными характеристиками.
- **Тело запроса** (JSON):
  ```json
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
  ```

### Получение информации о песне

- **URL**: `/api/songs/<int:pk>/`
- **Методы**: `GET`
- **Описание**: Позволяет получить информацию о песне по её id

### Обновление информации о песне

- **URL**: `/api/songs/<int:pk>/`
- **Методы**: `PUT`, `PATCH`
- **Описание**: Обновляет информацию о песне. `PUT` требует полного набора данных о песне, в то время как `PATCH` 
позволяет обновить только указанные поля.
- **Тело запроса** (JSON): Аналогично телу запроса для создания новой песни.

### Удаление песни

- **URL**: `/api/songs/<int:pk>/`
- **Метод**: `DELETE`
- **Описание**: Удаляет песню по её идентификатору.


## Примеры
```python
import requests


base_url = "http://127.0.0.1:8000/api/songs"

print(requests.get(base_url+"/1").json())
# output
# {'id': 1, 'tags': '', 'theme': '', 'genretype': '4.1', 'genre': 'Кантаты', 'author': 'Векшегонова И.', 'creationyear': '1971', 'composer': 'Чудова Татьяна Алексеевна', 'fullname': 'Богатыри'}

print(len(requests.get(base_url).json()))
# output
# 300

print(requests.post(base_url, data={'tags': 'test', 'theme': 'test', 'genretype': 'test4.1', 'genre': 'testКантаты',
                                    'author': 'testВекшегонова И.', 'creationyear': '1971',
                                    'composer': 'Чудова Татьяна Алексеевна test', 'fullname': 'Богатыри'}).status_code)
# output
# 201
```
