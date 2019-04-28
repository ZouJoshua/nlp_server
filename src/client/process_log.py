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

import os

base_dir = "/data/in_hi_news_parser_result"

tmp_result_file = "/data/parser_server_log_result"
ori_file = "/data/in_hi_html_random.json"
log_file = os.path.join(base_dir, "parser_server.log.2019-04-22")
final_result_file = os.path.join(base_dir, "hi_news_parser_20190421")



def ger_result_from_log(tmp_result_file):
    patten1 = re.compile(r"\[Successful parse html (.*?),")
    patten2 = re.compile(r"result:(\{.*?\})")

    f = open(log_file, 'r')
    # lines = f.readlines()[118056:]
    lines = f.readlines()
    f.close()
    _of = open(tmp_result_file, 'w')

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


# ger_result_from_log()

def get_parser_result(ori_file, log_file, final_result_file):

    f = open(ori_file, 'r')
    lines = f.readlines()[400000:]
    f.close()
    ori_dict = dict()

    for _line in lines:
        line = json.loads(_line.strip())
        if line:
            ori_dict[line['url']] = line['id']

    res_ = open(log_file, 'r')

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


def rewrite_result(file1, file2, new_file):
    old_f1 = open(file1, 'r')
    old_f2 = open(file2, 'r')
    new_f = open(new_file, 'w')
    old_list = old_f1.readlines() + old_f2.readlines()
    old = [i.strip() for i in old_list]
    new_list = dict()
    for i in old:
        line = json.loads(i)
        url = line['url']
        if url in new_list.keys():
            new_list[url] += 1
        else:
            new_list[url] = 1
            out = dict()
            for k, v in line.items():
                if k =='url':
                    out['url'] = line[k]
                else:
                    out['id'] = k
                    out['result'] = line[k]

            new_f.write(json.dumps(out) + "\n")


    old_f1.close()
    old_f2.close()
    new_f.close()


def rewrite_result_v1(file1, new_file):
    old_f1 = open(file1, 'r')
    new_f = open(new_file, 'w')
    old_list = old_f1.readlines()
    old = [i.strip() for i in old_list]
    new_list = dict()
    s = 0
    for i in old:
        line = json.loads(i)
        url = line['url']
        if url in new_list.keys():
            new_list[url] += 1
        else:
            new_list[url] = 1
            out = dict()
            s +=1
            for k, v in line.items():
                if k =='url':
                    out['url'] = line[k]
                else:
                    out['id'] = k
                    try:
                        if type(line[k]) ==dict:
                            out['result'] = line[k]
                        else:
                            out['result'] = json.loads(line[k].strip())
                    except :
                        print(s)
            new_f.write(json.dumps(out) + "\n")


    old_f1.close()
    new_f.close()



if __name__ == '__main__':
    file1 = os.path.join(base_dir, 'hi_news_parser_20190417')
    file2 = os.path.join(base_dir, 'hi_news_parser_20190417_')
    file_new = os.path.join(base_dir, 'parsered_hi_news_20190417')
    # rewrite_result(file1, file2, file_new)
    rewrite_result_v1(file1, file_new)