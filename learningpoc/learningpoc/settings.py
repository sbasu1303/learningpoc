"""
Django settings for learningpoc project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import sys
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0q64@rexld=jujwi4i)$4w%ykp4nw)hvq$bqoeur3!wzo2s_^g'

# SECURITY WARNING: don't run with debug turned on in production!
ENV = os.environ.get('DS_ENV', None)
if ENV == None and sys.platform == 'darwin':
    ENV = 'LOCAL'

if ENV in ['LOCAL', 'DEV']:
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'content_management',
    'user_management',
    'rest_core',
    'frontend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'learningpoc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'learningpoc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
databaseHost = '127.0.0.1'
databasePassword = '7H!^dt5C6%XG+UtY'
databaseEngine = 'django.db.backends.mysql'
databaseConnectionTimeOut = 3000
databasePort = '3306'

if ENV != 'LOCAL':
    databaseHost = 'host.docker.internal'

DATABASE_APPS_MAPPING = {
    'content_management' : 'learning_course_db',
    'user_management' : 'learning_course_db'
}


DATABASES = {
    'default':{
        'ENGINE': databaseEngine,
        'NAME': 'learning_core',
        'USER': 'lcore',
        'PASSWORD': databasePassword,
        'HOST': databaseHost,
        'PORT': databasePort,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': databaseConnectionTimeOut,
        }
    },
    'learning_course_db':{
        'ENGINE': databaseEngine,
        'NAME': 'learning_core',
        'USER': 'lcore',
        'PASSWORD': databasePassword,
        'HOST': databaseHost,
        'PORT': databasePort,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': databaseConnectionTimeOut,
        }
    }

}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOG_DIR = os.path.join(os.getenv('BASE_LOG_DIR'), 'ln_django')

loglevel = 'DEBUG'
if ENV == 'PROD':
    loglevel = 'INFO'


# SECURITY WARNING: don't run with debug turned on in production!
if ENV in ['LOCAL', 'DEV']:
    DEBUG = True
else:
    DEBUG = False


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s]| %(levelname)s| [%(name)s:%(lineno)s]| %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'custom': {
            'format': "[%(asctime)s]| %(levelname)s| [%(name)s:%(lineno)s]| %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'verbose': {
            'format': '%(levelname)s| %(asctime)s| %(module)s| %(process)d| %(thread)d| %(message)s'
        },
        'simple': {
            'format': '%(levelname)s| %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': loglevel,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        # 'sentry': {
        #     'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },
        'file': {
            'level': loglevel,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR+'/django_logs.log',
            'maxBytes': 1024*1024*500,
            'backupCount': 20,
            'encoding':'utf-8',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'learningpoc': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'rest_framework': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

S3_BUCKET_NAME = "dev-datasocle"
S3_ACCESS_KEY_ID = "AKIAJWZLDIGP4CKUREDA"
S3_SECRECT_ACCESS_KEY = "Yl72/RAK28JOPvUhya+NwwOEjTbOdIOsOuYR3g4Y"
