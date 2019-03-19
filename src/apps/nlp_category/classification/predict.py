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

    def get_category(self, content, title, classifier_dict, idx2label):
        """
        分类结果
        :param content: 内容（str）
        :param title: 标题（str）
        :param classifier_dict: 模型字典（dict）
        :param idx2label: 分类id映射（json）
        :param topk: 分类top n结果
        :return: 分类结果（一级类、二级类）
        """
        content_list = []
        content_list.append(self.clean_string(title + '.' + content))
        predict_top_res = self._predict_topcategory(content_list, classifier_dict, idx2label)
        # self.log.info("Successfully predicting the top_category\n{}".format(predict_top_res))
        predict_top_category = predict_top_res['top_category']
        if predict_top_category in classifier_dict.keys():
            classifier = classifier_dict[predict_top_category]
            # assert isinstance(classifier, SupervisedModel):
            predict_sub_res = self._predict_subcategory(content_list, classifier, idx2label, predict_top_res)
            # self.log.info("Successfully predicting the sub_category\n{}".format(predict_sub_res))
        else:
            predict_sub_res = predict_top_res
            self.log.warning("There is no secondary classification model for this primary classification({}).".format(predict_top_category))
        return predict_sub_res

    def get_topcategory(self, content_list, classifier_dict, idx2label):
        """
        一级分类结果
        :param content_list: 内容（list）
        :param classifier_dict: 模型字典（dict）
        :param idx2label: 分类id映射（json）
        :return: 一级分类结果（dict）
        """
        return self._predict_topcategory(content_list, classifier_dict, idx2label)

    def get_subcategory(self, content_list, classifier, idx2label, predict_res):
        """
        二级分类结果
        :param content_list: 内容（list）
        :param classifier: 二级分类模型（fasttext.model）
        :param idx2label: 分类id映射（json）
        :param predict_res: 一级分类结果
        :return: 二级分类结果
        """
        return self._predict_subcategory(content_list, classifier, idx2label, predict_res)

    def _predict_topcategory(self, content_list, classifier_dict, idx2label, topk=3):
        result = dict()
        result["topn_top_category"] = dict()
        try:
            classifier = classifier_dict['topcategory_model']
            label = classifier.predict_proba(content_list, topk)
        except Exception as e:
            self.log.error("Error({}) with topcategory model prediction.".format(e))
        else:
            for i in range(topk):
                predict_res = dict()
                predict_res['top_category_id'] = int(label[i][0][0].replace("__label__", ""))
                category = idx2label['topcategory'][label[i][0][0].replace("__label__", "")]
                predict_res['top_category'] = category
                predict_res['top_category_proba'] = label[i][0][1]
                if category == 'auto or science':
                    try:
                        auto_science_classifier = classifier_dict['auto_science']
                        auto_science_label = auto_science_classifier.predict_proba(content_list)
                    except Exception as e:
                        self.log.error("Error({}) with topcategory model 'auto or science' prediction.".format(e))
                    else:
                        predict_res['top_category_id'] = int(auto_science_label[i][0][0].replace("__label__", ""))
                        predict_res['top_category'] = idx2label['topcategory'][auto_science_label[i][0][0].replace("__label__", "")]
                        predict_res['top_category_proba'] = auto_science_label[i][0][1]
                result["topn_top_category"]["top{}".format(i+1)] = predict_res
            self.log.info("Successfully predicting the top_category\n{}".format(result))
        return result


    def _predict_subcategory(self, content_list, classifier, idx2label, category, topk=3):
        if category and isinstance(category, dict):
            predict_sub_res = category
            predict_sub_res["topn_sub_category"] = dict()
        else:
            self.log.warning("Request only subcategory.")
            predict_sub_res = dict()
            predict_sub_res["topn_sub_category"] = dict()
        try:
            label = classifier.predict_proba(content_list, topk)
        except Exception as e:
            self.log.error("Error({}) with secondary model prediction.".format(e))
        else:
            for i in range(topk):
                predict_res = dict()
                predict_res['sub_category_id'] = int(label[i][0][0].replace("__label__", ""))
                subcategory = idx2label['subcategory'][label[i][0][0].replace("__label__", "")]
                predict_res['sub_category'] = subcategory
                predict_res['sub_category_proba'] = label[i][0][1]
                predict_sub_res["topn_sub_category"]["top{}".format(i+1)] = predict_res
            self.log.info("Successfully predicting the sub_category\n{}".format(predict_sub_res))
        return predict_sub_res
