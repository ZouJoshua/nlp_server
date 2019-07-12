#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-7-10 下午6:34
@File    : normal_vtag_process.py
@Desc    : 多语言通用视频tag处理
"""

import re
import logging
import string
import emoji


class NormalProcess(object):

    def __init__(self, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("vtag_process")
            self.log.setLevel(logging.INFO)

    def get_cleaned_tag(self, taglist):
        new_tag_list = list()
        for tag in taglist:
            new_tag = self.trim_video_tag(tag)
            if new_tag:
                new_tag_list.append(new_tag)
        return new_tag_list

    def trim_video_tag(self, tag):
        _tag = self.clean_emoji(tag)
        _tag = self.clean_url(_tag)
        _tag = self.clean_mail(_tag)

        return _tag


    @staticmethod
    def clean_emoji(text):
        """
        清洗表情符号
        :param text:
        :return:
        """
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

    @staticmethod
    def clean_punc(text):
        """
        清洗标点符号
        :param text:
        :return:
        """
        del_symbol = string.punctuation  # ASCII 标点符号
        remove_punctuation_map = dict((ord(char), " ") for char in del_symbol)
        new_text = text.translate(remove_punctuation_map)  # 去掉ASCII 标点符号
        new_text = re.sub(r"\s+", " ", new_text).strip()
        return new_text

    @staticmethod
    def clean_mail(text):
        """
        清洗邮箱
        :param text:
        :return:
        """
        pattern = re.compile(r"\w+[-_.]*[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}")
        mail_list = re.findall(pattern, text)
        for mail in mail_list:
            text = text.replace(mail, " ")

    @staticmethod
    def clean_url(text):
        """
        清洗url网址
        :param text:
        :return:
        """
        pattern = re.compile(r'(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
        # pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+')
        url_list = re.findall(pattern, text)
        for url in url_list:
            text = text.replace(url, " ")
        return text.replace("( )", " ")