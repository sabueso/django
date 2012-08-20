import os
import sys
sys.path.append("/home/django")
os.environ['DJANGO_SETTINGS_MODULE'] = 'guars.settings'

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "test"
BROKER_PASSWORD = "password"
BROKER_VHOST = "vhost"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ('guars.tareas',)

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    "actualizacionmasterias60s": {
        "task": "guars.tareas.actualizacion",
        "schedule": timedelta(seconds=60),
        "args": ()
    },
}

