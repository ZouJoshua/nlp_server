#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/2/28 18:41
@File    : client.py
@Desc    : 爬虫解析客户端
"""

import requests
import json

url = 'http://127.0.0.1:8020/nlp_parser/parser'


id = "1502776564471413"
spider_url = 'https://theindianawaaz.com/president-confers-gandhi-peace-prize/'

# post 参数
parms = {"id": id, "website": spider_url}


## >>>>>>>>>> 请求爬虫解析服务参数
"""
传入参数：
    id: string（必传，打印日志）
    website: string（必传）
"""
# spider parser test
resp1 = requests.post(url, data=parms)  # 发送请求
print(resp1.text)

