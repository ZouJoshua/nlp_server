#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/2/28 18:41
@File    : client.py
@Desc    : 客户端
"""

import requests
import json


url = 'http://127.0.0.1:19901/nlp_category/category'
parms = {"title": "xxx", "content": "test"}

resp = requests.post(url, data=parms)  # 发送请求

# Decoded text returned by the request
text = resp.text
print(text)
# print(json.loads(text))

