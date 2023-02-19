# pull official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    # install pillow dependencies
    && apk add jpeg-dev zlib-dev libjpeg \
    # install django-allauth dependencies
    && apk add libffi-dev openssl-dev cargo \
    # install bash to run script
    && apk add bash

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
