from flask import Flask
from celery import Celery
import feedparser

#===============================================================================
# On windows go to the rabitmq-server/sbin and start rabbitmq-server.bat
# 1.: rabbitmq-server -detached
# Go to the dataCollector package in attomReader
# 2.: python -m celery -A tasks.celery worker --loglevel=info     // ctrl+c
#
# 3. rabbitmqctl stop
# rabbitmqctl status
#===============================================================================


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery



# main
flask_app = Flask(__name__)

flask_app.config['CELERY_BROKER_URL'] = 'amqp://guest@localhost//'
flask_app.config['CELERY_RESULT_BACKEND'] = 'amqp'

celery = make_celery(flask_app)
celery.conf.update(flask_app.config)


# tasks
@celery.task
def downloadFeeds(pageUrl):
    data = feedparser.parse(pageUrl)
    return pageUrl, data
