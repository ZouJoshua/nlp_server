#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-7-10 下午6:25
@File    : es_vtag_process.py
@Desc    : 西班牙语视频tag处理
"""


import logging
import re
import string


class EsProcess(object):

    def __init__(self, tag_dict, standard_tag_list, stopwords, logger=None):
        self.tag_dict = tag_dict
        self.standard_tag_list = standard_tag_list
        self.stopwords = stopwords

        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("vtag_process")
            self.log.setLevel(logging.INFO)

    def trim_video_tag(self, input_tag, tag_dict, standard_tag_list):
        self.log.info("")
        resultdict = {}
        details = []

        # 1. 预清洗
        new_tag = self.standard_tag(input_tag, standard_tag_list)
        # print(new_tag)
        tag_tokens = new_tag.split(" ")
        details.append("【{}】0==>【{}】".format(input_tag, new_tag))

        # 2. 预判断:is in tag_dict or not

        c_tag = []
        if len(tag_tokens) == 1:
            if new_tag in tag_dict.keys():
                c_tag = [new_tag]
        else:
            for tok in tag_tokens:
                if tok in tag_dict.keys():
                    print(new_tag)
                    print(tag_dict[tok].keys())
                    if new_tag in tag_dict[tok].keys():
                        c_tag = [new_tag]
                        print(c_tag)
                    else:
                        c_tag.append(tok)

        if len(c_tag) >= 1:
            resultdict["in_tag_dict"] = c_tag
            details.append("【{}】1==>【{}】".format(new_tag, c_tag))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(tag_tokens) < 2:
            resultdict["one_gram"] = [new_tag]
            details.append("【{}】2==>【{}】".format(new_tag, new_tag))
            return [new_tag], resultdict, details
        else:
            pass

        # 3.trim1 process: period trim 时间性单词 或修饰行状语

        pattern_period = r'^top\s{1}\d.\s{1}|^best|^best of|^hit|2015|2016|2017|2018|2019|latest|updates|today| new$|new released|^new '
        res_period = re.compile(pattern_period, flags=0)

        res1 = res_period.sub('', new_tag.strip())
        res1_tokens = []
        for w in res1.split(' '):
            w = w.strip()
            if w != '':
                res1_tokens.append(w)

        res1 = ' '.join(res1_tokens)

        res1findall = res_period.findall(new_tag.strip())
        resultdict['period'] = res1findall
        details.append("【{}】3==>【{}】".format(new_tag, res1))

        # 3. 预判断:is in tag_dict or not
        c_tag = []
        if len(res1_tokens) == 1:
            if res1 in tag_dict.keys():
                c_tag = [res1]
        else:
            for tok in res1_tokens:
                if tok in tag_dict.keys():
                    if res1 in tag_dict[tok].keys():
                        c_tag = res1_tokens
                    else:
                        c_tag.append(tok)

        if len(c_tag) >= 1:
            resultdict["period"] = c_tag
            details.append("【{}】4==>【{}】".format(res1, c_tag))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(res1_tokens) < 2:
            resultdict["period"] = [res1]
            details.append("【{}】5==>【{}】".format(new_tag, res1))
            return [res1], resultdict, details
        else:
            pass

        # 4.trim2 process: language trim

        pattern_lang = r'en español|español|españa|latino|latin|'

        res_lang = re.compile(pattern_lang, flags=0)
        res2 = res_lang.sub('', res1.strip())

        res2_tokens = []
        for w in res2.split(' '):
            w = w.strip()
            if w != '':
                res2_tokens.append(w)
        res2 = ' '.join(res2_tokens)

        res2findall = res_lang.findall(res1.strip())
        resultdict['lang'] = res2findall
        details.append("【{}】6==>【{}】".format(res1, res2))

        # 4. 预判断:is in tag_dict or not
        c_tag = []
        if len(res2_tokens) == 1:
            if res2 in tag_dict.keys():
                c_tag = [res2]
        else:
            for tok in res2_tokens:
                if tok in tag_dict.keys():
                    if res2 in tag_dict[tok].keys():
                        c_tag = res2_tokens
                    else:
                        c_tag.append(tok)

        if len(c_tag) >= 1:
            resultdict["lang"] = c_tag
            details.append("【{}】7==>【{}】".format(res1, c_tag))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(res1_tokens) < 2:
            resultdict["lang"] = [res2]
            details.append("【{}】\t8==>\t【{}】".format(new_tag, res2))
            return [res2], resultdict, details
        else:
            pass
        return [res2], resultdict, details

    def standard_tag(self, tag, standard_tag_list):
        # print(">>>>> 正在标准化tag")
        l_tag = tag.lower()
        tag = self.clean_url(l_tag)
        if tag.find("=") < 0 and tag.find("�") < 0:
            _tag = tag.replace("#0", "")
            year_tag = self.clean_period(_tag)
            if year_tag:
                no_punc_tag = _tag
            else:
                no_punc_tag = self.clean_punc(_tag)
            new_tag = self.proof_tag(no_punc_tag, standard_tag_list)
        else:
            new_tag = ""

        return new_tag.strip()

    @staticmethod
    def proof_tag(tag, standard_tag_list):
        """
        将tag标准化，如video变成videos
        :param tag:
        :param standard_tag_list:
        :return:
        """
        tag_len = tag.split(" ")
        if len(tag_len) == 1:
            if tag in standard_tag_list:
                return tag + "s"
            else:
                return tag
        else:
            new_tag = ""
            new_tmp_tag = ""
            replace_count = 0
            for tg in tag_len:
                if tg in standard_tag_list:
                    replace_count += 1
                    new_tmp_tag += "{}s ".format(tg)
                else:
                    new_tmp_tag += "{} ".format(tg)
            if replace_count < 2:
                new_tag = new_tmp_tag
            else:
                new_tag = tag
            return new_tag.strip()

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

    @staticmethod
    def clean_period(input_str):
        pattern_period = r'[1-2]\d{3}[s]{0,1}$|^\d{1,2}/\d{1,2}/^\d{2,4}$|\d{2,4}[-/]\d{2,4}$'
        res_period = re.compile(pattern_period, flags=0)
        mat = res_period.search(input_str)
        if mat:
            year_tag = mat.group(0)
        else:
            year_tag = ""
        return year_tag