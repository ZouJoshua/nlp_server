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
import emoji
from collections import Counter
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree


class EsProcess(object):

    def __init__(self, tag_dict, standard_tag_list, stopwords, logger=None):
        self.tag_dict = tag_dict
        self.standard_tag_list = standard_tag_list
        self.stopwords = stopwords

        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("nlp_v_tags_process")
            self.log.setLevel(logging.INFO)

    def get_cleaned_tags(self, taglist):
        self.log.info("Processing es video tag of taglist:【{}】".format(taglist))
        nlp_tags = list()
        for tag in taglist:
            _tags, _, _ = self.trim_video_tag(tag)
            nlp_tags += _tags

        nlp_tags_list = [k for k, v in Counter(nlp_tags).items() if len(k) > 2][:10]

        return [tag for tag in nlp_tags_list]

    def trim_video_tag(self, input_tag):
        resultdict = {}
        details = []

        # 1. 预清洗
        new_tag = self.standard_tag(input_tag, self.standard_tag_list)
        # print(new_tag)
        tag_tokens = new_tag.split(" ")
        details.append("【{}】0==>【{}】".format(input_tag, new_tag))

        # 2. 预判断:is in tag_dict or not

        c_tag = []
        if len(tag_tokens) == 1:
            if new_tag in self.tag_dict.keys():
                c_tag = [new_tag]
        else:
            for tok in tag_tokens:
                if tok in self.tag_dict.keys():
                    # print(new_tag)
                    # print(self.tag_dict[tok].keys())
                    if new_tag in self.tag_dict[tok].keys():
                        c_tag = [new_tag]
                        # print(c_tag)
                    else:
                        continue

        if len(c_tag) >= 1:
            resultdict["in_tag_dict"] = c_tag
            details.append("【{}】1==>【{}】".format(new_tag, c_tag))
            self.log.debug("Clean {} type tag details:{}".format("in_tag_dict", details))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(tag_tokens) < 2:
            resultdict["one_gram"] = [new_tag]
            details.append("【{}】2==>【{}】".format(new_tag, new_tag))
            self.log.debug("Clean {} type tag details:{}".format("one_gram", details))
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
            if res1 in self.tag_dict.keys():
                c_tag = [res1]
        else:
            for tok in res1_tokens:
                if tok in self.tag_dict.keys():
                    if res1 in self.tag_dict[tok].keys():
                        c_tag = [res1]
                    else:
                        continue

        if len(c_tag) >= 1:
            resultdict["period"] = c_tag
            details.append("【{}】4==>【{}】".format(res1, c_tag))
            self.log.debug("Clean {} type tag details:{}".format("period", details))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(res1_tokens) < 2:
            resultdict["period"] = [res1]
            details.append("【{}】5==>【{}】".format(new_tag, res1))
            self.log.debug("Clean {} type tag details:{}".format("period", details))
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
            if res2 in self.tag_dict.keys():
                c_tag = [res2]
        else:
            for tok in res2_tokens:
                if tok in self.tag_dict.keys():
                    if res2 in self.tag_dict[tok].keys():
                        c_tag = [res2]
                    else:
                        continue

        if len(c_tag) >= 1:
            resultdict["lang"] = c_tag
            details.append("【{}】7==>【{}】".format(res1, c_tag))
            self.log.debug("Clean {} type tag details:{}".format("lang", details))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(res1_tokens) < 2:
            resultdict["lang"] = [res2]
            details.append("【{}】8==>【{}】".format(new_tag, res2))
            self.log.debug("Clean {} type tag details:{}".format("lang", details))
            return [res2], resultdict, details
        else:
            pass
        return [res2], resultdict, details



    def extract_tag(self, title, text):
        self.log.info("Extracting tags from title and text...")
        mergetaglist = []
        mergetagdict = {}
        lasttaglist = []
        pattern1 = r"""(\||\-\s{1}|\s{1}\-|\(|\)|\?|!|–\s{1}|\s{1}–|│|\"|\'\s{1}|\s{1}\'|‘\s{1}|\s{1}‘|’\s{1}|\s{1}’|:|\s{1}\[|\]\s{1}|~|\/\s{1}|\s{1}\/|\*)"""
        res = re.compile(pattern1, flags=0)

        title_no_emoji = self.clean_emoji(title)
        title2 = res.sub("#", title_no_emoji)
        # print(title2)
        if text.startswith(title):
            text = text[len(title):]
        text2 = text.replace('\n', " ").replace("\t", " ").replace("\r", " ")
        text2 = self.clean_emoji(text2)
        text2 = self.clean_url(text2)
        text2 = self.clean_mail(text2)
        text2_lower = text2.lower()

        text2_ner_list = self.get_continuous_chunks(text2_lower)
        self.log.info("Extracting tags from text 【{}】".format(text2_ner_list))
        # print(text2_ner_list)

        title_ner_list = list()
        for title_trunk in title2.split('#'):
            title_trunk = title_trunk.strip()
            title_trunk_lower = title_trunk.lower()
            title_trunk_tokens = title_trunk_lower.split(" ")

            if title_trunk != '':
                if len(title_trunk_tokens) == 1:
                    if title_trunk_lower not in mergetagdict:
                        mergetaglist.append([title_trunk_lower, 'title_trunk_vtag'])
                        mergetagdict[title_trunk_lower] = None
                elif len(title_trunk_tokens) < 5:

                    for tok in title_trunk_tokens:
                        if tok in self.tag_dict:
                            if title_trunk_lower not in mergetagdict:
                                mergetaglist.append([title_trunk_lower, 'title_trunk_kw'])
                                mergetagdict[title_trunk_lower] = None
                        else:
                            if len(title_trunk_tokens) < 3 and title_trunk_lower not in mergetagdict:
                                mergetaglist.append([title_trunk_lower, 'title_trunk_kw'])
                                mergetagdict[title_trunk_lower] = None

                elif len(title_trunk_tokens) >= 5:
                    for tok in title_trunk_tokens:
                        if tok in self.tag_dict:
                            if tok not in mergetagdict and len(tok) > 3:
                                mergetaglist.append([tok, 'title_trunk_kw'])
                                mergetagdict[tok] = None
                else:
                    continue

            title_trunk_list = self.get_continuous_chunks(title_trunk)
            # print(">>>>> title_trunk:{}".format(title_trunk))
            # print(">>>>> title_trunk_list:{}".format(title_trunk_list))
            title_ner_list.extend(title_trunk_list)

        self.log.info("Extracting tags from title 【{}】".format(title_ner_list))

        tfdict = dict()
        for trunk in title_ner_list:
            trunk_lower = trunk.lower()
            if trunk_lower == '': continue
            if trunk_lower in self.stopwords: continue
            if len(trunk_lower) < 4: continue
            n = len(trunk_lower.split(' '))
            x = 1.5
            if n >= 2:
                x = 2
            if trunk_lower not in tfdict:
                tfdict[trunk_lower] = x
            else:
                tfdict[trunk_lower] += x

        for trunk in text2_ner_list:
            trunk_lower = trunk.lower()
            if trunk_lower in self.stopwords: continue
            if trunk_lower == '': continue
            if len(trunk_lower) < 4: continue
            if trunk_lower not in tfdict:
                tfdict[trunk_lower] = 1
            else:
                tfdict[trunk_lower] += 1
        sorted_tfdict = sorted(tfdict.items(), key=lambda k: k[1], reverse=True)
        sorted_tfdict2 = [x for x in sorted_tfdict if x[1] >= 2]

        for c_tag, c_tf in sorted_tfdict2:

            if c_tag in self.tag_dict or len(c_tag.split(' ')) >= 2:
                if c_tag not in mergetagdict:
                    mergetaglist.append([c_tag, 'tf_vtag'])
                    mergetagdict[c_tag] = None

        for i, (tag, reason) in enumerate(mergetaglist):
            if i >= 5: break
            lasttaglist.append(tag)

        return lasttaglist

    def get_continuous_chunks(self, text):

        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                continuous_chunk.append(" ".join(current_chunk))
                continuous_chunk.append(i[0])
                current_chunk = []
            else:
                continuous_chunk.append(i[0])
                continue
        if current_chunk:
            continuous_chunk.append(" ".join(current_chunk))
            current_chunk = []

        return continuous_chunk



    def standard_tag(self, tag, standard_tag_list):
        # print(">>>>> 正在标准化tag")
        l_tag = tag.lower()
        tag = self.clean_url(l_tag)
        if tag.find("=") < 0 and tag.find("�") < 0:
            if not tag.isdigit():
                _tag = tag.replace("#0", "")
                year_tag = self.clean_period(_tag)
                if year_tag:
                    no_punc_tag = _tag.replace(year_tag, "")
                else:
                    no_punc_tag = self.clean_punc(_tag)
                new_tag = self.proof_tag(no_punc_tag, standard_tag_list)
            else:
                new_tag = ""
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
        return text

    @staticmethod
    def clean_url(text):
        """
        清洗url网址
        :param text:
        :return:
        """
        pattern = re.compile(
            r'(?:(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])|(?:www\.[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])')
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