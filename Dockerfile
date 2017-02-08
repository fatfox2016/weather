# Ubuntu 14.04，Trusty Tahr（可靠的塔尔羊）发行版
FROM ubuntu:trusty


MAINTAINER weather <wuli4444@163.com>

# APT 自动安装 Python 相关的依赖包，如需其他依赖包在此添加
RUN apt-get update && \
    apt-get install -y python3.5 \
                       python-dev \
                       python-pip  \
    # 用完包管理器后安排打扫卫生可以显著的减少镜像大小
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 



RUN mkdir -p /app
COPY . /app
WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD [""]