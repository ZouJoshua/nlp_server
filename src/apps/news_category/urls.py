#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/1/29 14:44
@File    : urls.py
@Desc    : 
"""

from django.urls import path
from .views import index_view
from .views import TopCategory, SubCategory, Category


app_name = '[news_category]'

urlpatterns = [
    path('', index_view, name='index_url'),
    path('category', Category.as_view()),
    path('top', TopCategory.as_view()),
    path('sub', SubCategory.as_view()),
]