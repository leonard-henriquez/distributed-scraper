from celery import Celery
from .settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

from datadog import initialize
initialize(statsd_host='datadog')

print('URL of broker: ', CELERY_BROKER_URL)
print('URL of backend: ', CELERY_RESULT_BACKEND)

app = Celery(
  'worker',
  broker = CELERY_BROKER_URL,
  backend = CELERY_RESULT_BACKEND,
)

app.conf.update(
  include = ['worker.tasks'],
  task_default_queue = 'default_queue',
  task_routes = {
    'worker.tasks.add_download': {'queue': 'download_queue'},
    'worker.tasks.add_source': {'queue': 'source_queue'}
    },
  task_default_delivery_mode = "persistent",
  result_persistent = True
)

if __name__ == '__main__':
  app.start()
