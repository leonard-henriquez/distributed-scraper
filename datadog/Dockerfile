FROM alpine AS builder

ARG REDIS_PASS
ARG RABBITMQ_USER
ARG RABBITMQ_PASS


ADD ./conf.d/ /tmp/conf.d/
WORKDIR /tmp/conf.d/

RUN apk add gettext && \
  envsubst '$$RABBITMQ_USER $$RABBITMQ_PASS' < rabbitmq.yaml > rabbitmq.yaml && \
  envsubst '$$REDIS_PASS' < redisdb.yaml > redisdb.yaml



FROM datadog/agent:latest
RUN rm /etc/datadog-agent/conf.d/redisdb.d/auto_conf.yaml
COPY --from=builder /tmp/conf.d/rabbitmq.yaml /etc/datadog-agent/conf.d/
COPY --from=builder /tmp/conf.d/redisdb.yaml /etc/datadog-agent/conf.d/
