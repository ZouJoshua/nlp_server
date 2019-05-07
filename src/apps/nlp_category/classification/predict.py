#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/4 12:26
@File    : predict.py
@Desc    : 
"""

from pyquery import PyQuery
import re
import logging
import json
import requests



class Predict(object):

    def __init__(self, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("load_classification_model")
            self.log.setLevel(logging.INFO)

    # 全模型用于清洗正文数据
    def clean_string(self, text):
        # 清洗html标签
        doc = PyQuery(text)
        text = doc.text()
        # 去除网址和邮箱
        text = text.replace("\n", "").replace("\t", "").replace("\r", "").replace("&#13;", "").lower()
        url_list = re.findall(r'http://[a-zA-Z0-9.?/&=:]*', text)
        for url in url_list:
            text = text.replace(url, "")
        email_list = re.findall(r"[\w\d\.-_]+(?=\@)", text)
        for email in email_list:
            text = text.replace(email, "")
        # 去除诡异的标点符号
        cleaned_text = ""
        for c in text:
            if (ord(c) >= 65 and ord(c) <= 126) or (ord(c) >= 32 and ord(c) <= 63):
                cleaned_text += c
        return cleaned_text

    def get_category(self, top_c, sub_c, idx2label):
        """
        分类结果
        :param top_c: 一级分类id（str）
        :param sub_c: 二级分类id（str）
        :param r_type: 分类类型（0：文章 1：视频）
        :param b_type: 分类业务类型（0:浏览器 1:游戏）
        :return: 分类结果（一级类、二级类）
        """
        if sub_c in idx2label.keys():
            predict_res = idx2label[sub_c]
            self.log.info("Successfully predicting the sub_category\n{}".format(predict_res))
            return predict_res
        else:
            self.log.warning("Secondary classification id does not exist")
            if top_c in idx2label.keys():
                predict_res = idx2label[top_c]
                self.log.info("Successfully predicting the top_category\n{}".format(predict_res))
                return predict_res
            else:
                predict_res = {"top_category": [{"id": top_c, "category": "", "proba": 0.0}],
                                "sub_category": [{"id": sub_c, "category": "", "proba": 0.0}]}
                self.log.error("Primary classification id does not exist")
                return predict_res
