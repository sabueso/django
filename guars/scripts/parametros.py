import os
import sys
sys.path.insert(0, "/home/django/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'guars.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

