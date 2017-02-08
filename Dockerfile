FROM daocloud.io/python:3.5
MAINTAINER weather <wuli4444@163.com>

RUN mkdir -p /app
COPY . /app
WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 5000


CMD command python /app/weatherWeb.py runserver