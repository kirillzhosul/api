# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'
ENV POETRY_HOME='/usr/local'

# Project directory.
WORKDIR /srv/www/kirillzhosul/api

# Install requirements.
COPY pyproject.toml .
RUN pip install poetry && poetry install --no-ansi --no-interaction

# Copy whole project.
COPY . /srv/www/kirillzhosul/api/

# Run project.
CMD ["gunicorn", "app.app:app", "-c", "gunicorn.conf.py"]
