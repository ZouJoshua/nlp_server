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

class BaseConfig(object):
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

    ROOT_URLCONF = 'web.urls'

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

    WSGI_APPLICATION = 'web.wsgi.application'
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

    def __init__(self):


        # 添加 apps 目录
        sys.path.insert(0, os.path.join(self.BASE_DIR, 'apps'))

        # 添加 utils 目录
        sys.path.insert(0, os.path.join(self.BASE_DIR, 'utils'))

        # 日志
        DEFAULT_LOGGING_LEVEL = logging.INFO
        PROJECT_LOGS_PATH = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(PROJECT_LOGS_PATH):
            os.mkdir(PROJECT_LOGS_PATH)

        # NLP数据目录
        PROJECT_DATA_PATH = os.path.join(self.BASE_DIR, 'data')

        CATEGORY_LOG_FILE = os.path.join(PROJECT_LOGS_PATH, 'category_server.log')
        REGIONAL_LOG_FILE = os.path.join(PROJECT_LOGS_PATH, 'regional_server.log')
        PARSER_LOG_FILE = os.path.join(PROJECT_LOGS_PATH, 'parser_server.log')

        # NLP分类模型路径
        NLP_MODEL_PATH = os.path.join(PROJECT_DATA_PATH, 'model')
        # NLP_MODEL_PATH = '/data/zoushuai/news_content/sub_classification_model/model'
