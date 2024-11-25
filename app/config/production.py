from .base import *
import json
import os
from decouple import config

DEBUG = False


ALLOWED_HOSTS = [config('DJANGO_DOMAIN'),'localhost']

# Asignar las variables de configuración desde el JSON
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DJANGO_DB_NAME'),
        'USER': config('DJANGO_DB_USER'),
        'PASSWORD': config('DJANGO_DB_PASSWORD'),
        'HOST': config('DJANGO_DB_HOST'),
        'PORT': config('DJANGO_DB_PORT'),
    }
}

SECRET_KEY = config('DJANGO_SECRET_KEY')
#os.environ['DJANGO_SETTINGS_MODULE'] = config['DJANGO_SETTINGS_MODULE']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django_debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}