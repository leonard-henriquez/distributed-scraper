FROM datadog/agent:latest
RUN rm /etc/datadog-agent/conf.d/redisdb.d/auto_conf.yaml
ADD conf.d/rabbitmq.yaml /etc/datadog-agent/conf.d/rabbitmq.yaml
ADD conf.d/redisdb.yaml /etc/datadog-agent/conf.d/redisdb.yaml
