#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-7-15 下午3:25
@File    : v_tag_client_test.py
@Desc    : 西班牙语vtag处理测试
"""

import os
import sys
curr_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(curr_dir)
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "utils"))
print(sys.path)

import requests
from utils.tools import read_json_format_file

url = 'http://127.0.0.1:9022/polls/vtag'


def tt_es_tag_server(raw_file):
    print(">>>>> 正在读取西班牙原始tag")
    count_ = 0
    for line in read_json_format_file(raw_file):
        _id = line["id"]
        title = line["article_title"]
        content = line["text"]
        vtaglist = line["vtaglist"]
        lang = line["lang"]
        # lang = "eg"
        parms = {"newsid": _id, "lang": lang, "title": title, "vtaglist": vtaglist, "content": content}
        resp = requests.post(url, data=parms)  # 发送请求
        print("\n>>>>> id:【{}】".format(_id))
        print(">>>>> raw vtaglist:【{}】".format(vtaglist))
        print(">>>>> nlp vtaglist:【{}】".format(resp.text.replace("\t", ",")))
        count_ += 1
        if count_ == 1000:
            break


def tt_ko_tag_server(raw_file):
    print(">>>>> 正在读取韩国原始tag")
    count_ = 0
    for line in read_json_format_file(raw_file):
        _id = line["id"]
        title = line["article_title"]
        content = line["text"]
        vtaglist = line["vtaglist"]
        lang = line["lang"]
        # lang = "eg"
        parms = {"newsid": _id, "lang": lang, "title": title, "vtaglist": vtaglist, "content": content}
        resp = requests.post(url, data=parms)  # 发送请求
        print("\n>>>>> id:【{}】".format(_id))
        print(">>>>> raw vtaglist:【{}】".format(vtaglist))
        print(">>>>> nlp vtaglist:【{}】".format(resp.text.replace("\t", ",")))
        count_ += 1
        if count_ == 1000:
            break


# es_raw_file = "/home/zoushuai/algoproject/algo-python/nlp/preprocess/tags/ES_video_tags"
# tt_es_tag_server(es_raw_file)
# ko_raw_file = "/home/zoushuai/algoproject/algo-python/nlp/preprocess/tags/KR_video_tags"
# tt_ko_tag_server(ko_raw_file)
de_raw_file = "/home/zoushuai/algoproject/algo-python/nlp/preprocess/tags/DE_video_tags"
tt_ko_tag_server(de_raw_file)