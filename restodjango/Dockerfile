FROM python:3.11.2-alpine
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN apk update && apk add bash \  
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
