FROM python:3.7-alpine3.9

WORKDIR /tmp

RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.9/main" >> /etc/apk/repositories && \
  echo "http://dl-cdn.alpinelinux.org/alpine/v3.9/community" >> /etc/apk/repositories

# install chromedriver
RUN apk add --update gcc g++ gcc libxslt-dev chromium chromium-chromedriver

WORKDIR /
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

ADD . /worker
CMD ["celery", "worker", "-A", "worker.worker", "--queues=download_queue,source_queue", "-n worker@%h", "--loglevel=info"]
