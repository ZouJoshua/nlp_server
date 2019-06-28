#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-5-10 上午9:51
@File    : video_category_conf.py
@Desc    : 视频分类服务配置
"""


import os
import sys
import logging


###############
#Basic Setting#
###############

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 添加 apps 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# print(sys.path)
# 添加 utils 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))
# print(sys.path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dxj13rzpw*(h%ew#vk5rbmj-rh%i(*kvp*m^ll_kxvkxdoc@-)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = ['*', ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'


# CACHESps -ef | g
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}



# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
#     }
# }


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'



# 日志
DEFAULT_LOGGING_LEVEL = logging.INFO
LOG_PATH = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# NLP数据目录
PROJECT_DATA_PATH = os.path.join(BASE_DIR, 'data')

################
#Server Setting#
################

NLP_SERVER_NAME = os.environ.get("NLP_SERVER_NAME", 'video_tags')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 添加nlp分类app
    'apps.{}'.format(NLP_SERVER_NAME),
]

PROJECT_LOG_FILE = os.path.join(LOG_PATH, '{}_server.log'.format(NLP_SERVER_NAME))

# nlp模型
NLP_MODEL_PATH = os.path.join(PROJECT_DATA_PATH, NLP_SERVER_NAME)
# NLP_MODEL_PATH = '/data/zoushuai/news_content/sub_classification_model/model'