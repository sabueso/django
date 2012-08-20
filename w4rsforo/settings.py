# Django settings for mysite project.
#
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('sabueso', 'sabueso@sabueso.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = 'djangow4rs'             # Or path to database file if using sqlite3.
DATABASE_NAME ='bdforo'
DATABASE_USER = 'django'             # Not used with sqlite3.
DATABASE_PASSWORD = 'passdejemplo'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
INTERNAL_IPS = ('127.0.0.1',)
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#EDIA_ROOT = '/usr/share/python-support/python-django/django/contrib/admin/media'
MEDIA_ROOT = '/usr/lib/python2.5/site-packages/django/contrib/admin/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://foro.w4rs.com/media'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&jgi*8*4%^g(mx)92-wwr8x()_pu)s3!7)fl#oa+xjnpmgaiwc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
#	'djangologging.middleware.LoggingMiddleware',
    'django.template.loaders.app_directories.load_template_source',
     'django.template.loaders.eggs.load_template_source'
)
#TEMPLATE_CONTEXT_PROCESSORS =(
#		'django.contrib.auth.context_processors.auth',
#		'django.core.context_processors.debug',
#		'django.core.context_processors.i18n',
#		'django.core.context_processors.media',
#		'django.contrib.messages.context_processors.messages'
#)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'w4rsforo.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	"/home/django/w4rsforo/templates"
)

INSTALLED_APPS = (
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.sites',
'django.contrib.comments',
'django.contrib.admin',
'tinymce',
'registration',
'w4rsforo.foro'
)

import logging
logging.basicConfig(
		level = logging.DEBUG,
		format = '%(asctime)s %(levelname)s %(message)s',
		filename = '/tmp/foro.log',
		filemode = 'w'
		)


ACCOUNT_ACTIVATION_DAYS = 7

TINYMCE_JS_URL = 'http://foro.w4rs.com/media/js/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace",
    'theme': "advanced",
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

LOGIN_REDIRECT_URL="/"
