#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-9 下午5:20
@File    : data_p.py
@Desc    : 
"""


import json

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