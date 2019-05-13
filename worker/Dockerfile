FROM python:3.7-alpine3.9

RUN apk add --update g++ gcc libxslt-dev

WORKDIR /
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

ADD . /worker
CMD ["celery", "worker", "-A", "worker.worker", "--queues=download_queue,source_queue", "-n worker@%h", "--loglevel=info"]
