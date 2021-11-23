FROM python:3.7.12-buster
# ARG VERSION=99.0.0

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

# Do not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Do not ever buffer console output
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
RUN pip install supervisor

COPY poetry.lock pyproject.toml README.md /app/
COPY src /app/src/
COPY supervisord.conf /app
RUN mkdir /app/var && mkdir /app/var/log && mkdir /app/var/mail && mkdir /app/var/sms && mkdir /app/var/gcm

WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install

RUN useradd -ms /bin/bash behaving

RUN chown -R behaving /app

USER behaving

# Just wait forever
# ENTRYPOINT ["tail"]
# CMD ["sleep", "infinity"]

ENTRYPOINT [ "supervisord" ]
