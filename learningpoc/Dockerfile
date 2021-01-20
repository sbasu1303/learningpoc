FROM ubuntu:18.04

MAINTAINER sbasu1303

# Install required packages and remove the apt packages cache when done.
RUN mkdir -p /usr/lib/uwsgi/plugins
RUN apt-get update && apt-get upgrade -y && apt-get install -y apt-utils
RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get --fix-missing install -y \
    software-properties-common \
	git \
	default-jre \
	openjdk-11-jre-headless \
	openjdk-8-jre-headless\
	python3.8 \
	python3.8-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	systemd \
	sqlite3 \
	apt-utils \
	python3-software-properties \
	cron \
	curl \
	libpython3.8-dev \
	libpangocairo-1.0-0 \
	libx11-xcb1 \
	libxcomposite1 \
	libxcursor1 \
	libxdamage1 \
	libxi6 \
	libxtst6 \
	libnss3 \
	libcups2 \
	libxss1 \
	libxrandr2 \
	libgconf-2-4 \
	libasound2 \
	libatk1.0-0 \
	libgtk-3-0 \
	vim \
	gconf-service \
	libappindicator1 \
	libc6 \
	libcairo2 \
	libcups2 \
	libdbus-1-3 \
	libexpat1 \
	libfontconfig1 \
	libgcc1 \
	libgdk-pixbuf2.0-0 \
	libglib2.0-0 \
	libnspr4 \
	libpango-1.0-0 \
	libstdc++6 \
	libx11-6 \
	libxcb1 \
	libxext6 \
	libxfixes3  \
	libxrender1 \
	libxtst6 \
	libssl-dev \
	redis-tools \
	libmysqlclient-dev\
	ca-certificates \
	fonts-liberation \
	lsb-release \
	xdg-utils \
	wget \
	openssl \
	gcc \
	sudo \
	net-tools \
	iputils-ping \
	mysql-client\
	uwsgi \
	uwsgi-plugin-python3 \
	poppler-utils \
	libpq-dev && \
   rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/
ENV APP_DIR /usr/src/app/
ENV PYTHONPATH /usr/bin/python3.8

RUN python3.8 -m pip install --upgrade pip setuptools wheel
RUN mkdir -p $APP_DIR/logs
RUN mkdir -p $APP_DIR/logs/uwgsi

COPY . /usr/src/app
RUN rm -rf $APP_DIR/.git
RUN rm -f $APP_DIR/.gitignore

RUN mkdir -p $APP_DIR/media