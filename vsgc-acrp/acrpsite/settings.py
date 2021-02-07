"""
Django settings for acrpsite project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.contrib import messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bfo%v50iwa8z&si6m4f)!2^mwhhp!vrgcie*qzozn0oug=zvxb'
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['vsgcapps.odu.edu','128.82.98.60','[::1]','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'acrpapp.apps.AcrpappConfig',
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
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

ROOT_URLCONF = 'acrpsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
		        'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'acrpsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "acrpsite",
#         'USER': 'rbond001',#'zubair',
#         'PASSWORD':'J8e4MYjS7365eREn',# 'sahil92',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "vsgc",
        'USER': 'root',#'zubair',
        'PASSWORD':'',# 'sahil92',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

import stat

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FILE_UPLOAD_PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR,'static/')
CRISPY_TEMPLATE_PACK='bootstrap4'
MESSAGE_TAGS={
    messages.DEBUG:'alert-info',
    messages.INFO:'alert-info',
    messages.SUCCESS:'alert-success',
    messages.WARNING:'alert-warning',
    messages.ERROR:'alert-danger',
}

MEDIA_ROOT=os.path.join(BASE_DIR,'media/')
#MEDIA_ROOT= '/opt/vsgc-acrp/vsgc-acrp/media/'
MEDIA_URL = 'media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "rbond4747@gmail.com"
EMAIL_HOST_PASSWORD = 'Bindupp:1327'
EMAIL_PORT = '587'
