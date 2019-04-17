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
import requests
base_path = os.path.dirname((os.path.dirname(os.path.realpath(__file__))))
sys.path.append(base_path)
sys.path.append(os.path.join(base_path, 'web'))
from web.settings import PROJECT_LOG_FILE, PROJECT_DATA_PATH

url = 'http://127.0.0.1:8020/nlp_parser/parser'


#>>>>>>>>>> test <<<<<<<<<<#

data_file = os.path.join(PROJECT_DATA_PATH, 'test', 'hi_news_test.txt')
result_file = os.path.join(PROJECT_DATA_PATH, 'test', 'result20190416')

#>>>>>>>>>> prod <<<<<<<<<<#

# data_file = '/data/zoushuai/news_content/html/dt=2019-04-11/url_random'
# result_file = '/data/zoushuai/result20190416'


NLP_PARSER_FILE_PATH = os.path.join(PROJECT_DATA_PATH, 'rules.json')


def main():
    with open(NLP_PARSER_FILE_PATH, 'r', encoding='utf-8') as jf:
        rules_xpath = json.load(jf)
    _of = open(result_file, "w")
    with open(data_file, 'r') as f:
        i = 0
        while True:
            i += 1
            if i < 10:
                line = json.loads(f.readline())
                _url = line['url']
                domain = urlparse(_url).netloc
                id = line['id']
                parms = {'id': id, 'website': _url, "lang": "hi"}
                resp = requests.post(url, data=parms)
                if resp.status_code != 408:
                    out = {str(id): resp.text, "url": _url}
                else:
                    nu = {"category": [], "title": [], "tag": [], "hyperlink_text": [], "hyperlink_url": []}
                    out = {str(id): nu, "url": _url}
                _of.write(json.dumps(out) + '\n')
                sys.stdout.flush()
                _of.flush()
            else:
                _of.close()
                break

if __name__ == '__main__':
    main()
    # print(NLP_PARSER_FILE_PATH)
