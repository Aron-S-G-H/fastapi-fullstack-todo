FROM python:3.10-slim

LABEL maintainer="aronesadegh@gmail.com"

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=off
ENV POETRY_VERSION=1.8.2
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

ENV DATABASE_NAME=your_db_name
ENV DATABASE_USERNAME=your_db_username
ENV DATABSE_PASSWORD=your_db_password

WORKDIR /source

COPY . /source/

ARG INDEX=https://mirror-pypi.runflare.com/simple
ARG INDEX-URL=https://mirror-pypi.runflare.com/simple
ARG TRUSTED-HOST=mirror-pypi.runflare.com

RUN apt-get update -y && apt-get upgrade -y

RUN pip config --user set global.index ${INDEX} &&  pip config --user set global.index-url ${INDEX-URL} &&  pip config --user set global.trusted-host ${TRUSTED-HOST}

RUN pip install -U pip && pip install -r requirements.txt

EXPOSE 8000

RUN alembic upgrade head

CMD ["uvicorn", "settings:app", "--host", "0.0.0.0", "--port", "8000"]