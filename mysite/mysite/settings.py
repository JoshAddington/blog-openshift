"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if 'BLOG_SECRET' in os.environ:
    SECRET_KEY = os.environ['BLOG_SECRET']
else:
    SECRET_KEY = '(w48h&fdpz4-y9s+svv470#%!7n1h&c&7kvj1aj5c*1oj-(mvr'

# SECURITY WARNING: don't run with debug turned on in production!
if 'DJ_DEBUG' in os.environ:
    DEBUG = (os.environ['DJ_DEBUG'] == 'True')
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

INSTALLED_APPS += (
    'blog',
    'citibike',
    'debug_toolbar',
    'djcelery',
    'kombu.transport.django',
    'projects',
    'rest_framework',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/'),
            os.path.join(BASE_DIR, 'citibike/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if DEBUG is False:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['CODE_DB_NAME'],
            'USER': os.environ['CODE_USERNAME'],
            'PASSWORD': os.environ['CODE_PASSWORD'],
            'HOST': os.environ['CODE_ENDPOINT'],
            'PORT': os.environ['CODE_PORT'],
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Grappelli template settings
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'www', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'citibike', 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# AWS S3 Bucket settings

AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_S3_DOMAIN = "s3.amazonaws.com/%s" % AWS_STORAGE_BUCKET_NAME
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Media file storage

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'




# RabbitMQ settings
BROKER_URL = "amqp://%s:%s@localhost:5672/%s" % (
    os.environ['RABBITMQ_USER'],
    os.environ['RABBITMQ_PASSWORD'],
    os.environ['RABBITMQ_VHOST'])

# Celery Settings
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
