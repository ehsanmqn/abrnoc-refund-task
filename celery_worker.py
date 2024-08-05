from app import create_app
from celery import Celery
from celery.schedules import crontab

app = create_app()


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_BACKEND'],
        broker=app.config['CELERY_BROKER']
    )
    celery.conf.update(
        imports=['app.tasks'],
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

celery.conf.beat_schedule = {
    'check_status-every-30-minutes': {
        'task': 'app.tasks.check_status',
        'schedule': crontab(minute='*/1'),  # Runs every 30 minutes
    },
}

celery.conf.timezone = 'UTC'