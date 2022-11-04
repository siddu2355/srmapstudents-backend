from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fqdvepw*xtl@r^vb(lk_f*f^m*=c=@b%zqyf*d!s2uw@0^m6tt'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'srmapstudents',
        'HOST':'localhost',
        'USER':'root',
        'PASSWORD':'#$iddu2355'
    }
}
