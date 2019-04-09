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

url = 'http://127.0.0.1:8020/nlp_parser/parser'

# spider parser test
with open("/home/zoushuai/algoproject/nlp_parser_server/src/data/url_test.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        parms = dict()
        lj = json.loads(line)
        parms['id'] = lj['id']
        parms['website'] = lj['url']
        resp = requests.post(url, data=parms)  # 发送请求
        print(resp.text)

