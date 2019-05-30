#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/4 12:26
@File    : predict.py
@Desc    : 
"""

import fasttext
from pyquery import PyQuery
import re
import logging


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

    def get_category(self, content, title, model, idx2label, thresholds=0.3):
        """
        分类结果
        :param content: 内容（str）
        :param title: 标题（str）
        :param classifier_dict: 模型字典（dict）
        :param idx2label: 分类id映射（json）
        :param topk: 分类topk结果(默认)
        :return: 分类结果（一级类、二级类）
        """
        content_list = []
        content_list.append(self.clean_string(title + '.' + content))
        predict_res = self._predict_category(content_list, model, idx2label, proba_threshold=thresholds)
        return predict_res

    def _predict_category(self, content_list, model, idx2label, topk=3, proba_threshold=0.3):
        result = dict()
        result["taste_category"] = list()
        try:
            label = model.predict_proba(content_list, topk)
        except Exception as e:
            self.log.error('Error({}) with taste category model prediction.'.format(e))
        else:
            for i in range(topk):
                predict_res = dict()
                predict_res['id'] = int(label[0][i][0].replace('__label__', ''))
                category = idx2label[label[0][i][0].replace('__label__', '')]
                predict_res['category'] = category
                predict_res['proba'] = label[0][i][1]
                if i == 0:
                    predict_res['proba'] = float('%.6f' % (predict_res['proba'] + 0.000001))
                    if predict_res['proba'] >= 1.0:
                        predict_res['proba'] = 1.0
                if predict_res['proba'] < proba_threshold and i != 0:
                    # predict_res_less_than_theashold = {'id': -1, 'category': '', 'proba': 0.0}
                    continue
                else:
                    result['taste_category'].append(predict_res)
            self.log.info('Successfully predicting the taste category\n{}'.format(result))
        return result



