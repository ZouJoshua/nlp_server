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

    def get_category(self, content, title, classifier_dict, idx2label, thresholds=(0.3,0.2)):
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
        if thresholds and len(thresholds) == 2:
            top_threshold, sub_threshold = thresholds
        else:
            top_threshold, sub_threshold = (0.3, 0.2)
        predict_top_res = self._predict_topcategory(content_list, classifier_dict, idx2label, proba_threshold=top_threshold)
        # self.log.info("Successfully predicting the top_category\n{}".format(predict_top_res))
        predict_top_category = predict_top_res['top_category'][0]['category']
        if predict_top_category in classifier_dict.keys():
            classifier = classifier_dict[predict_top_category]
            # assert isinstance(classifier, SupervisedModel):
            predict_sub_res = self._predict_subcategory(content_list, classifier, idx2label, predict_top_res, proba_threshold=sub_threshold)
            # self.log.info("Successfully predicting the sub_category\n{}".format(predict_sub_res))
        else:
            predict_top_res['sub_category'] = list()
            predict_sub_res = predict_top_res
            self.log.warning("There is no secondary classification model for this primary classification({}).".format(predict_top_category))
        return predict_sub_res

    def get_topcategory(self, content_list, classifier_dict, idx2label, threshold=0.3):
        """
        一级分类结果
        :param content_list: 内容（list）
        :param classifier_dict: 模型字典（dict）
        :param idx2label: 分类id映射（json）
        :return: 一级分类结果（dict）
        """
        return self._predict_topcategory(content_list, classifier_dict, idx2label, proba_threshold=threshold)

    def get_subcategory(self, content_list, classifier, idx2label, predict_res, threshold=0.2):
        """
        二级分类结果
        :param content_list: 内容（list）
        :param classifier: 二级分类模型（fasttext.model）
        :param idx2label: 分类id映射（json）
        :param predict_res: 一级分类结果
        :return: 二级分类结果
        """
        return self._predict_subcategory(content_list, classifier, idx2label, predict_res, proba_threshold=threshold)

    def _predict_topcategory(self, content_list, classifier_dict, idx2label, topk=3, proba_threshold=0.3):
        result = dict()
        result["top_category"] = list()
        try:
            classifier = classifier_dict['topcategory_model']
            label = classifier.predict_proba(content_list, topk)
        except Exception as e:
            self.log.error('Error({}) with topcategory model prediction.'.format(e))
        else:
            for i in range(topk):
                predict_res = dict()
                predict_res['id'] = int(label[0][i][0].replace('__label__', ''))
                category = idx2label['topcategory'][label[0][i][0].replace('__label__', '')]
                predict_res['category'] = category
                predict_res['proba'] = label[0][i][1]
                if category == 'auto or science':
                    try:
                        auto_science_classifier = classifier_dict['auto_science']
                        auto_science_label = auto_science_classifier.predict_proba(content_list)
                    except Exception as e:
                        self.log.error("Error({}) with topcategory model 'auto or science' prediction.".format(e))
                    else:
                        predict_res['id'] = int(auto_science_label[0][i][0].replace('__label__', ''))
                        predict_res['category'] = idx2label['topcategory'][auto_science_label[0][i][0].replace('_label__', '')]
                        predict_res['proba'] = auto_science_label[0][i][1]
                if i == 0:
                    predict_res['proba'] = float('%.6f' % (predict_res['proba'] + 0.000001))
                    if predict_res['proba'] >= 1.0:
                        predict_res['proba'] = 1.0
                if predict_res['proba'] < proba_threshold and i != 0:
                    # predict_res_less_than_theashold = {'id': -1, 'category': '', 'proba': 0.0}
                    continue
                else:
                    result['top_category'].append(predict_res)
            self.log.info('Successfully predicting the top_category\n{}'.format(result))
        return result


    def _predict_subcategory(self, content_list, classifier, idx2label, category, topk=3, proba_threshold=0.2):
        if category and isinstance(category, dict):
            predict_sub_res = category
            predict_sub_res['sub_category'] = list()
        else:
            self.log.warning('Request only subcategory.')
            predict_sub_res = dict()
            predict_sub_res['sub_category'] = list()
        try:
            label = classifier.predict_proba(content_list, topk)
        except Exception as e:
            self.log.error('Error({}) with secondary model prediction.'.format(e))
        else:
            for i in range(topk):
                predict_res = dict()
                predict_res['id'] = int(label[0][i][0].replace('__label__', ''))
                subcategory = idx2label['subcategory'][label[0][i][0].replace('__label__', '')]
                predict_res['category'] = subcategory
                predict_res['proba'] = label[0][i][1]
                if i == 0:
                    predict_res['proba'] = float('%.6f' % (label[0][i][1] + 0.000001))
                    if predict_res['proba'] >= 1.0:
                        predict_res['proba'] = 1.0
                if i != 0 and predict_res['proba'] < proba_threshold:
                    # predict_sub_res_less_than_threshold = {'id': -1, 'category': '', 'proba': 0.0}
                    continue
                else:
                    predict_sub_res['sub_category'].append(predict_res)
            self.log.info('Successfully predicting the sub_category\n{}'.format(predict_sub_res))
        return predict_sub_res
