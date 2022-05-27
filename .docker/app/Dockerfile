# pull official base image
FROM python:3.8.13-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Ho_Chi_Minh

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev freetype-dev tzdata

# install dependencies
RUN pip install --upgrade pip

RUN mkdir -p requirements
ADD ./requirements ./requirements
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# copy project
COPY . .

ENTRYPOINT [ "./.docker/app/entrypoint.sh" ]
