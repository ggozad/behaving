FROM aerokube/selenoid:latest-release
ARG BUILDPLATFORM
ARG DOWNLOAD_VOLUME

RUN apk add gettext

COPY browsers.json.template /etc/selenoid/browsers.json.template
RUN export CHROME_IMAGE=$([ "${BUILDPLATFORM}" = "linux/arm64" ] && echo "sskorol/selenoid_chromium_vnc:100.0" || echo "selenoid/chrome") && \
    envsubst < /etc/selenoid/browsers.json.template > /etc/selenoid/browsers.json
