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

id1 = "1502764925793848"
parser_url1 = "http://www.bollywoodnews.org/go/WlZTp"
parms1 = {"id": id1, "website": parser_url1, "lang": "en"}

id2 = "1502776564471413"
parser_url2 = "https://www.sciencedaily.com/releases/2019/02/190225123449.htm"
parms2 = {"id": id2, "website": parser_url2, "lang": "en"}

id3 = "1502889409622478"
parser_url3 = "https://theindianawaaz.com/president-confers-gandhi-peace-prize/"
parms3 = {"id": id3, "website": parser_url3, "lang": "en"}



# spider parser test
resp1 = requests.post(url, data=parms1)  # 发送请求
# Decoded text returned by the request
print(resp1.text)

resp2 = requests.post(url, data=parms2)  # 发送请求
# Decoded text returned by the request
print(resp2.text)

resp3 = requests.post(url, data=parms3)  # 发送请求
# Decoded text returned by the request
print(resp3.text)