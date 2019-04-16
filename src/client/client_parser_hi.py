#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-16 下午8:04
@File    : client_parser_hi.py
@Desc    : 解析印地语客户端
"""


import random
import json
import os
import sys
from urllib.parse import urlparse
from web.settings import PROJECT_LOG_FILE, PROJECT_DATA_PATH
import requests

url = 'http://127.0.0.1:8020/nlp_parser/parser'

NLP_EN_PARSER_FILE_PATH = os.path.join(PROJECT_DATA_PATH, 'rules.json')

with open(NLP_EN_PARSER_FILE_PATH, 'r', encoding='utf-8') as jf:
    rules_xpath = json.load(jf)

_of = open("/data/zoushuai/result20190416", "w")

with open("/data/zoushuai/news_content/html/dt=2019-04-11/part-00000-674b9c2b-4ee2-435d-beb8-55d25d781687-c000.json", 'r') as f:
    i = 0
    while True:
        i += 1
        if i < 300000:
            line = json.loads(f.readline())
            _url = line['url']
            domain = urlparse(_url).netloc
            id = line['resource_id']
            parms = {'id': id, 'website': _url, "lang": "hi"}
            resp = requests.post(url, data=parms)
            out = {str(id): resp, "url": _url}
            _of.write(json.dumps(out) + '\n')
            sys.stdout.flush()
            _of.flush()
        else:
            _of.close()
            break
