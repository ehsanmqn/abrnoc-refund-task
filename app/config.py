import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-my-secrets'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

    KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS') or 'localhost:9092'
    REFUND_TOPIC = os.environ.get('REFUND_TOPIC') or 'refund_requests'
