#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-10 下午6:16
@File    : global_conf.py
@Desc    : 
"""

import os
import sys
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'dxj13rzpw*(h%ew#vk5rbmj-rh%i(*kvp*m^ll_kxvkxdoc@-)'
DEBUG = False
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'


# 添加 apps 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 添加 utils 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))

# 日志
DEFAULT_LOGGING_LEVEL = logging.INFO
PROJECT_LOGS_PATH = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(PROJECT_LOGS_PATH):
    os.mkdir(PROJECT_LOGS_PATH)

# server环境
if os.environ.get("NLP_SERVER_NAME"):
    NLP_SERVER_NAME = os.environ.get("NLP_SERVER_NAME")
else:
    raise Exception("服务名称环境设置错误，请检查...")

# server数据目录
PROJECT_DATA_PATH = os.path.join(BASE_DIR, 'data')


# 服务日志
DEFAULT_LOG_FILE = os.path.join(PROJECT_LOGS_PATH, '{}_server.log'.format(NLP_SERVER_NAME))

