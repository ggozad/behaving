FROM aerokube/selenoid:latest-release
ARG BUILDPLATFORM
ARG DOWNLOAD_VOLUME

RUN apk add gettext

COPY browsers.json.template /etc/selenoid/browsers.json.template
RUN envsubst < /etc/selenoid/browsers.json.template > /etc/selenoid/browsers.json
