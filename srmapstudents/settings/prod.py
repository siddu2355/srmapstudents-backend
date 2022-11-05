import os
from .common import *
import django_heroku

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#Allowed hosts only required when debug is false
ALLOWED_HOSTS = ['afternoon-plains-69747.herokuapp.com']

SECRET_KEY = 'siddu235463'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd62kt72v247l77',
        'HOST':'ec2-35-170-21-76.compute-1.amazonaws.com',
        'USER':'gndchvlkratekn',
        'PASSWORD':'aed1a1aeebd73377ae719f581201a3cf79cef24e58a654e21e3923fcc291778e',
        'PORT':'5432',
    }
}
AUTH_USER_MODEL="core.user"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
django_heroku.settings(locals())