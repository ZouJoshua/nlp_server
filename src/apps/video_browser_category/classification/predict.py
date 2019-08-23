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
import emoji
import string



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

    def clean_content(self, text):
        text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        text = text.lower()
        cd_instance = CleanDoc(text)
        no_emoji = cd_instance.remove_emoji(text)
        no_url = cd_instance.clean_html(no_emoji)
        no_mail = cd_instance.clean_mail(no_url)
        no_symbol = cd_instance.remove_symbol(no_mail)
        text = re.sub(r"\s+", " ", no_symbol)
        return text


    def get_category(self, title, content, tags, classifier_dict, idx2label, thresholds=(0.3,0.2)):
        """
        分类结果
        :param content: 内容（str）
        :param title: 标题（str）
        :param tags: 视频tag（）
        :param classifier_dict: 模型字典（dict）
        :param idx2label: 分类id映射（json）
        :param topk: 分类topk结果(默认)
        :return: 分类结果（一级类）
        """
        content_list = []
        ori_text = title + " " + content + " " + tags
        text = self.clean_content(ori_text)
        content_list.append(text)
        if thresholds and len(thresholds) == 2:
            top_threshold, sub_threshold = thresholds
        else:
            top_threshold, sub_threshold = (0.3, 0.2)
        predict_top_res = self._predict_topcategory(content_list, classifier_dict, idx2label, proba_threshold=top_threshold)
        # self.log.info("Successfully predicting the top_category\n{}".format(predict_top_res))
        return predict_top_res

    def _predict_topcategory(self, content_list, classifier_dict, idx2label, topk=3, proba_threshold=0.3):
        result = dict()
        result["top_category"] = list()
        try:
            classifier = classifier_dict['topcategory_model']
            label = classifier.predict_proba(content_list, topk)
            label_id = label[0][0][0].replace('__label__', '')
            if label_id == "200":
                sub_classifier = classifier_dict['topcategory_sub_model']
                label = sub_classifier.predict_proba(content_list, topk)
        except Exception as e:
            self.log.error('Error({}) with topcategory model prediction.'.format(e))
        else:
            for i in range(topk):
                predict_res = dict()
                predict_res['id'] = int(label[0][i][0].replace('__label__', ''))
                category = idx2label['topcategory'][label[0][i][0].replace('__label__', '')]
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
                    result['top_category'].append(predict_res)
            self.log.info('Successfully predicting the top_category\n{}'.format(result))
        return result




class CleanDoc(object):

    def __init__(self, text):
        self.text = self.clean_text(text)

    def clean_text(self, text):
        """
        清洗流程
        step1 -> 替换掉换行符、制表符等
        step2 -> 转小写
        step3 -> 清洗网址
        step4 -> 清洗邮箱
        step5 -> 清洗表情等非英文字符
        step6 -> 清洗标点符号、数字
        step7 -> 替换多个空格为一个空格
        :param text: 原始文本
        :return: 清洗后的文本
        """
        text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        _text = text.lower()
        no_html = self.clean_html(_text)
        no_mail = self.clean_mail(no_html)
        no_emoji = self.remove_emoji(no_mail)
        no_symbol = self.remove_symbol(no_emoji)
        text = re.sub(r"\s+", " ", no_symbol)
        return text

    def remove_en_emoji(self, text):
        cleaned_text = ""
        for c in text:
            if (ord(c) >= 65 and ord(c) <= 126) or (ord(c) >= 32 and ord(c) <= 63):
                cleaned_text += c
        return cleaned_text

    def remove_emoji(self, text):
        token_list = text.replace("¡", "").replace("¿", "").split(" ")
        em_str = r":.*?:"
        em_p = re.compile(em_str, flags=0)
        clean_token = list()
        for token in token_list:
            em = emoji.demojize(token)
            emj = em_p.search(em)
            if emj:
                _e = emj.group(0)
                # print(_e)
            else:
                clean_token.append(token)
        cleaned_text = " ".join(clean_token)
        return cleaned_text.strip()

    def clean_html(self, text):
        """
        去除网址
        1.完整网址https开头的
        2.没有协议头的网址，www开头的
        :param text:
        :return:
        """

        pattern = re.compile(
            r'(?:(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])|(?:www\.[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])')
        # pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+')
        # url_list = re.findall(pattern, text)
        # for url in url_list:
        #     text = text.replace(url, " ")
        text = pattern.sub("", text)
        return text.replace("( )", " ")

    def clean_mail(self, text):
        # 去除邮箱
        pattern = re.compile(r"\w+[-_.]*[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}")
        text = pattern.sub(" ", text)
        # mail_list = re.findall(pattern, text)
        # for mail in mail_list:
        #     text = text.replace(mail, " ")
        return text

    def remove_symbol_and_digits(self, text):
        del_symbol = string.punctuation + string.digits  # ASCII 标点符号，数字
        remove_punctuation_map = dict((ord(char), " ") for char in del_symbol)
        text = text.translate(remove_punctuation_map)  # 去掉ASCII 标点符号
        return text

    def remove_symbol(self, text):
        del_symbol = string.punctuation  # ASCII 标点符号
        remove_punctuation_map = dict((ord(char), " ") for char in del_symbol)
        text = text.translate(remove_punctuation_map)  # 去掉ASCII 标点符号
        return text