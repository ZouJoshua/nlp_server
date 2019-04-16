#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-9 下午5:20
@File    : data_p.py
@Desc    : 
"""


import json
import random

def write_url_test_file():
    nf = open("/data/url_test.txt", "w")
    with open("/data/content.json", 'r') as f:
        i = 0
        while True:
            i += 1
            line = json.loads(f.readline())
            url = line['url']
            id = line['resource_id']
            result ={'id':id, 'url': url}
            nf.write(json.dumps(result)+"\n")
            if i > 1000:
                break
    nf.close()


def write_url_random():
    nf = open("/data/zoushuai/news_content/html/dt=2019-04-11/url_random", "w")
    with open(
        "/data/zoushuai/news_content/html/dt=2019-04-11/part-00000-674b9c2b-4ee2-435d-beb8-55d25d781687-c000.json",
        'r') as f:
        lines = f.readlines()
        random.shuffle(lines)
        for i in lines:
            nf.write(json.dumps(i.strip()) + "\n")
    nf.close()


write_url_random()