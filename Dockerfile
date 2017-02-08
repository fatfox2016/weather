FROM daocloud.io/python:3.5
MAINTAINER weather <wuli4444@163.com>

RUN mkdir -p /app
COPY . /app
WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt


EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["weatherWeb.py"]
