import time
import click
from os import environ
from datetime import datetime, timedelta
from celery import Celery

def get_worker(broker, backend):
  worker = Celery(
    'worker',
    broker=broker,
    backend=backend,
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
  return worker


def add_task(worker, tag, start_date, end_date):
  date = end_date
  while date >= start_date:
    str_date = date.strftime("%Y/%m/%d")
    click.echo("Adding archive from {date} to download source".format(date=str_date))

    args = ("data-science", str_date)
    worker.send_task('worker.tasks.add_source', args=args)
    date = date - timedelta(days=1)


@click.command()
@click.argument('tags')
@click.option('--start-date', '-a', help='Date to begin scrapping (YYYY/MM/DD)')
@click.option('--end-date', '-z', help='Date to end scrapping (YYYY/MM/DD)')
@click.option('--broker', '-b', help='Date to end scrapping (YYYY/MM/DD)')
@click.option('--backend', '-e', help='Date to end scrapping (YYYY/MM/DD)')
def main(tags, start_date, end_date, broker, backend):
  """Simple program to scrap medium by tags"""
  today = datetime.now().strftime("%Y/%m/%d")

  start_date = start_date or today
  start_date = datetime.strptime(start_date, "%Y/%m/%d")

  end_date = end_date or today
  end_date = datetime.strptime(end_date, "%Y/%m/%d")

  broker = broker or environ["CELERY_BROKER_URL"]
  backend = backend or environ["CELERY_RESULT_BACKEND"]

  click.echo('URL of broker: {broker}'.format(broker=broker))
  click.echo('URL of backend: {backend}'.format(backend=backend))

  worker = get_worker(broker, backend)


  for tag in tags.split(','):
    click.echo("Tag selected: {tag}".format(tag=tag))
    click.echo("Starting adding new items to download source...")
    add_task(worker, tag, start_date, end_date)
    click.echo("Done!")


if __name__ == '__main__':
  main()
