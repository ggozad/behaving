FROM debian:jessie
MAINTAINER Yiorgis Gozadinos

RUN apt-get update

# Install nodejs repositories
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -

# Install python, node & dependencies
RUN apt-get -y install python-dev python2.7-dev python-pip nodejs

# Install utils
RUN apt-get -y install wget unzip xvfb

# Install Chrome, chromedriver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update
RUN apt-get -y install google-chrome-stable
WORKDIR /usr/local/bin
RUN wget http://chromedriver.storage.googleapis.com/2.21/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN rm chromedriver_linux64.zip
RUN chmod a+rx chromedriver

# Install firefox
RUN sh -c 'echo "deb http://packages.linuxmint.com debian import" >> /etc/apt/sources.list.d/firefox.list'
RUN gpg --keyserver pgpkeys.mit.edu --recv-key 3EE67F3D0FF405B2
RUN gpg -a --export 3EE67F3D0FF405B2 | apt-key add -
RUN apt-get update
RUN apt-get -y install firefox

WORKDIR /root
COPY . behaving
COPY templates/docker-run.sh /root/docker-run.sh
RUN chmod +x /root/docker-run.sh
RUN cd behaving && \
    python bootstrap.py && \
    ./bin/buildout

ENTRYPOINT ["sh", "/root/docker-run.sh"]
CMD ["tests/features"]