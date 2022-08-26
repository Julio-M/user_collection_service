# pull the official docker image
FROM python:3.9.4-slim

#set work directory
WORKDIR /services

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./services/authentication/requirements.txt .
RUN \
  python3 -m pip install -r requirements.txt --no-cache-dir && apt-get update && apt-get install make

# copy project
COPY . .