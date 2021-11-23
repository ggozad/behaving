FROM python:3.7.12-buster
# ARG VERSION=99.0.0

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

# Do not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Do not ever buffer console output
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/
COPY src /app/src/

WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
# COPY docker/runner /usr/bin/runner
RUN mkdir /app/var && mkdir /app/var/mail && mkdir /app/var/sms && mkdir /app/var/gcm

RUN \
    adduser --disabled-password --disabled-login --system testuser
RUN chown -R testuser /app


USER testuser

# Just wait forever
ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]

# ENTRYPOINT ["behave"]
# CMD ["--no-capture","tests/features"]
