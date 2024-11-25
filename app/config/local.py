from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-@!3o0w+s(j2#ua2)8cg26t@_$oyfgcvk5@g(ud*ao&n0-m$&u^'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]