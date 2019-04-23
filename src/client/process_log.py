#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-19 下午6:44
@File    : process_log.py
@Desc    : 日志提取
"""

import re
import json
log_file = "/data/in_hi_news_parser_result/parser_server.log.2019-04-20"
result_file = "/data/parser_server_log_result"


def ger_result_from_log():
    patten1 = re.compile(r"\[Successful parse html (.*?),")
    patten2 = re.compile(r"result:(\{.*?\})")

    f = open(log_file, 'r')
    lines = f.readlines()[118056:]
    f.close()
    _of = open(result_file, 'w')

    for i in range(len(lines)):
        url = re.findall(patten1, lines[i])
        if len(url) == 1 and i+1 < len(lines):
            result = re.findall(patten2, lines[i+1])
            if len(result) == 1:
                out = dict()
                out['url'] = url[0]
                out['result'] = result[0]
                _of.write(json.dumps(out) + "\n")
            continue

    _of.close()


ger_result_from_log()

ori_file = "/data/in_hi_html_random.json"

f = open(ori_file, 'r')
lines = f.readlines()[400000:3000000]
f.close()
ori_dict = dict()

for _line in lines:
    line = json.loads(_line.strip())
    if line:
        ori_dict[line['url']] = line['id']

res_ = open(result_file, 'r')

final_result_file = "/data/in_hi_news_parser_result/hi_news_parser_20190420_log_result"

out_ = open(final_result_file, 'w')
while True:
    r_dict = dict()
    line_ = res_.readline().strip()
    if line_:
        r_line = json.loads(line_)
        url_ = r_line['url']
        if url_ in ori_dict.keys():
            _id = ori_dict[url_]
            r_dict[_id] = r_line['result']
            r_dict['url'] = url_
            out_.write(json.dumps(r_dict) + '\n')
        else:
            continue
    else:
        out_.close()
        break
