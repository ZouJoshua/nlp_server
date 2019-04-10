#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/1/29 14:44
@File    : urls.py
@Desc    : 
"""

from django.urls import path

from .views import SpiderParser


app_name = '[nlp_parser]'

urlpatterns = [
    path('parser', SpiderParser.as_view()),
]