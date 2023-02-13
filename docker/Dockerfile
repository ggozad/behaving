FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8


# Do not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Do not ever buffer console output
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip poetry pip install supervisor

COPY poetry.lock pyproject.toml README.md config/supervisord.conf .gherkin-lintrc /app/
COPY src /app/src/
RUN mkdir /app/var && mkdir /app/var/log && mkdir /app/var/mail && mkdir /app/var/sms && mkdir /app/var/gcm && mkdir /app/var/downloads

WORKDIR /app
RUN poetry config virtualenvs.create false && poetry install
RUN useradd -ms /bin/bash behaving && chown -R behaving /app
USER behaving

ENTRYPOINT [ "supervisord" ]
