import time
from os import environ
from datetime import datetime
from celery import Celery

CELERY_BROKER_URL = environ["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = environ["CELERY_RESULT_BACKEND"]

print('URL of broker: ', CELERY_BROKER_URL)
print('URL of backend: ', CELERY_RESULT_BACKEND)
worker = Celery(
  'worker',
  broker=CELERY_BROKER_URL,
  backend=CELERY_RESULT_BACKEND,
)

worker.conf.update(
  include=['worker.tasks'],
  task_default_queue='default_queue',
  task_routes={
    'worker.tasks.add_download': {'queue': 'download_queue'},
    'worker.tasks.add_source': {'queue': 'source_queue'}
  },
  task_default_delivery_mode="persistent",
  result_persistent=True
)


print('Start!')
for i in range(1, 10):
  print('New task #', i)
  date = datetime(2018, 1, i).strftime("%Y/%m/%d")
  result = worker.send_task('worker.tasks.add_source', args=("data-science", date))

exit()
