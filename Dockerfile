FROM python:3.11.4-slim

LABEL maintainer="kostia3507@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt  requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head
