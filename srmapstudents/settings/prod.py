import os
from .common import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#Allowed hosts only required when debug is false
ALLOWED_HOSTS = ['srmapstudents-prod.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default':dj_database_url.config()
}
import psycopg2