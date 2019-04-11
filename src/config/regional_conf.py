#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-11 上午9:44
@File    : regional_conf.py
@Desc    : nlp_regional_server setting
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
# 添加 utils 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))

SECRET_KEY = 'dxj13rzpw*(h%ew#vk5rbmj-rh%i(*kvp*m^ll_kxvkxdoc@-)'

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

ROOT_URLCONF = 'server.urls'
WSGI_APPLICATION = 'server.wsgi.application'


# Database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
#     }
# }


# Password validation

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'


# 日志
DEFAULT_LOGGING_LEVEL = logging.INFO
PROJECT_LOGS_PATH = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(PROJECT_LOGS_PATH):
    os.mkdir(PROJECT_LOGS_PATH)

# NLP数据目录
PROJECT_DATA_PATH = os.path.join(BASE_DIR, 'data')


################
#Server Setting#
################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 添加nlp地域app
    'apps.nlp_regional',

]

REGIONAL_LOG_FILE = os.path.join(PROJECT_LOGS_PATH, 'regional_server.log')
