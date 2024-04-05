FROM python:3.12.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POSTGRES_USER=exampleuser
ENV POSTGRES_PASSWORD=examplepassword
ENV POSTGRES_DB=exampledb

RUN apt-get update \
    && apt-get install -y netcat-openbsd postgresql postgresql-contrib \
    && service postgresql start \
    && su - postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\"" \
    && su - postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;\""

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]