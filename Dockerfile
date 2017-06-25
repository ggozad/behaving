FROM python:2
MAINTAINER Denis Kadyshev

ARG FIREFOX_VERSION=53.0
ARG GECKODRIVER_VERSION=0.16.1

ARG CHROME_VERSION=google-chrome-stable
ARG CHROME_DRIVER_VERSION=2.30

ARG PHANTOMJS_VERSION=1.9.8

ARG CORDOVA_VERSION=4.3.0

# Following line fixes https://github.com/SeleniumHQ/docker-selenium/issues/87
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# No interactive frontend during docker build
ENV DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true

ENV TZ "UTC"
RUN echo "${TZ}" > /etc/timezone && dpkg-reconfigure tzdata

# Install requirements
RUN curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -qq && apt-get -qqy install locales \
        ${CHROME_VERSION:-google-chrome-stable} \
        libfreetype6 libfontconfig1 unzip bzip2 xvfb \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

## Firefox
RUN curl -fsSLo /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
    && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
    && rm /tmp/firefox.tar.bz2 \
    && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
    && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox
RUN curl -fsSLo /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
    && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
    && rm /tmp/geckodriver.tar.gz \
    && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
    && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
    && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver

## Chrome webdriver
RUN curl -fsSLo /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /opt \
    && rm /tmp/chromedriver_linux64.zip \
    && mv /opt/chromedriver /opt/chromedriver-$CHROME_DRIVER_VERSION \
    && chmod 755 /opt/chromedriver-$CHROME_DRIVER_VERSION \
    && ln -fs /opt/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver
### FIXME: Workaround for chrome in docker
RUN mv -v /opt/google/chrome/google-chrome /opt/google/chrome/google-chrome.dist \
    && echo '/opt/google/chrome/google-chrome.dist --no-sandbox $@' > /opt/google/chrome/google-chrome \
    && chmod +x /opt/google/chrome/google-chrome

## PhantomJS
RUN curl -fsSLo /tmp/phantomjs-${PHANTOMJS_VERSION}-linux-x86_64.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-${PHANTOMJS_VERSION}-linux-x86_64.tar.bz2 \
    && tar -C /opt -xjf /tmp/phantomjs-${PHANTOMJS_VERSION}-linux-x86_64.tar.bz2 \
    && rm /tmp/phantomjs-${PHANTOMJS_VERSION}-linux-x86_64.tar.bz2 \
    && ln -s /opt/phantomjs-${PHANTOMJS_VERSION}-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs

WORKDIR /root
COPY . behaving
RUN install -m 755 behaving/templates/docker-run.sh /root/docker-run.sh \
    && cd behaving \
    && python bootstrap.py \
    && ./bin/buildout

ENTRYPOINT ["/bin/sh", "/root/docker-run.sh"]
CMD ["tests/features"]
