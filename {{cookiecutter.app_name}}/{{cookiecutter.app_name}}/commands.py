import click
from flask.cli import AppGroup

from celery.bin import worker as celery_worker


celery_cli = AppGroup('celery')


@celery_cli.command(with_appcontext=False)
@click.option('--concurrency', default=None, help='Concurrency', type=click.INT)
@click.option('--loglevel', default=None, help='loglevel')
def worker(concurrency=None, loglevel='INFO'):
    """Run celery worker."""
    from {{cookiecutter.app_name}}.extensions import celery
    celery_worker.worker(app=celery).run(
        loglevel=loglevel, concurrency=concurrency
    )
