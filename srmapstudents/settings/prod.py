import os
from .common import *
import dj_database_url
import django_heroku

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#Allowed hosts only required when debug is false
ALLOWED_HOSTS = ['srmapstudents-prod.herokuapp.com']

SECRET_KEY = 'siddu235463'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deqjagmmhhf616',
        'HOST':'ec2-44-209-24-62.compute-1.amazonaws.com',
        'USER':'yvzlpzgxznojoy',
        'PASSWORD':'67e9223fcc93300e35d9ec294b2f886a330f79749c5a3fa2a4a742e27cd2e419',
        'PORT':'5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
django_heroku.settings(locals())