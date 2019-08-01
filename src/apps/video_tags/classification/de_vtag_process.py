#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-7-25 上午9:55
@File    : de_vtag_process.py
@Desc    : 德语视频tag处理
"""


import logging
import re
import string
import emoji
import langdetect
from collections import Counter
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree


class DeProcess(object):

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
        self.log.info("Processing de video tag of taglist:【{}】".format(taglist))
        nlp_tags = list()
        for tag in taglist:
            _tags, _, _ = self.trim_video_tag(tag)
            nlp_tags += _tags

        nlp_tags_list = [k for k, v in Counter(nlp_tags).items() if len(k) > 2][:6]

        return [tag for tag in nlp_tags_list]

    def trim_video_tag(self, input_tag):
        resultdict = {}
        details = []

        # 1. 预清洗
        new_tag = self.pre_clean(input_tag)
        # print(new_tag)
        soccer_patten = re.compile("\d-\d|\d:\d|\d \d")
        no_num_tag = soccer_patten.sub("", new_tag).strip()

        if no_num_tag:
            if no_num_tag.find(" vs ") >= 0:
                tag_tokens = no_num_tag.split(" vs ")
            elif no_num_tag.find(" - ") >= 0:
                tag_tokens = no_num_tag.split(" - ")
            elif no_num_tag.find(".") >= 0:
                tag_tokens = no_num_tag.split(".")
            else:
                tag_tokens = no_num_tag.split("\n")
        else:
            resultdict["sorccer"] = no_num_tag
            details.append("【{}】0==>【{}】".format(new_tag, no_num_tag))
            self.log.debug("Clean {} type tag details:{}".format("sorccer", details))
            return no_num_tag, resultdict, details

        # 2. 预判断:is in tag_dict or not

        c_tag = []
        if len(tag_tokens) == 1:
            if no_num_tag in self.tag_dict.keys():
                c_tag = [no_num_tag]
        else:
            for tok in tag_tokens:
                if tok in self.tag_dict.keys():
                    c_tag.append(tok)
                    # print(new_tag)
                    # print(self.tag_dict[tok].keys())
                    if no_num_tag in self.tag_dict[tok].keys():
                        c_tag.append(no_num_tag)
                        # print(c_tag)
                    else:
                        continue

        if len(c_tag) >= 1:
            resultdict["in_tag_dict"] = c_tag
            details.append("【{}】1==>【{}】".format(no_num_tag, c_tag))
            self.log.debug("Clean {} type tag details:{}".format("in_tag_dict", details))
            return c_tag, resultdict, details
        else:
            pass

        # 小于2元词不处理,直接返回
        if len(tag_tokens) < 2:
            resultdict["one_gram"] = [no_num_tag]
            details.append("【{}】2==>【{}】".format(no_num_tag, no_num_tag))
            self.log.debug("Clean {} type tag details:{}".format("one_gram", details))
            return [no_num_tag], resultdict, details
        else:
            pass

        # 3.trim1 process: period trim 时间性单词 或修饰行状语

        pattern_period = r'^top\s{1}\d.\s{1}|^best|^best of|^hit|2015|2016|2017|2018|2019|latest|updates|today| new$|new released|^new '
        res_period = re.compile(pattern_period, flags=0)

        res1 = res_period.sub('', no_num_tag.strip())
        res1_tokens = []
        for w in res1.split(' '):
            w = w.strip()
            if w != '':
                res1_tokens.append(w)

        res1 = ' '.join(res1_tokens)

        res1findall = res_period.findall(no_num_tag.strip())
        resultdict['period'] = res1findall
        details.append("【{}】3==>【{}】".format(no_num_tag, res1))

        # 3. 预判断:is in tag_dict or not
        c_tag = []
        if len(res1_tokens) == 1:
            if res1 in self.tag_dict.keys():
                c_tag.append(res1)
        else:
            for tok in res1_tokens:
                if tok in self.tag_dict.keys():
                    c_tag.append(tok)
                    if res1 in self.tag_dict[tok].keys():
                        c_tag.append(res1)
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
            details.append("【{}】5==>【{}】".format(no_num_tag, res1))
            self.log.debug("Clean {} type tag details:{}".format("period", details))
            return [res1], resultdict, details
        else:
            pass

        return [res1], resultdict, details
        # # 4.trim2 process: language trim
        #
        # pattern_lang = r'in korean$|in korea$|of korea$|^korean|^korea|korea$'
        #
        # res_lang = re.compile(pattern_lang, flags=0)
        # res2 = res_lang.sub('', res1.strip())
        #
        # res2_tokens = []
        # for w in res2.split(' '):
        #     w = w.strip()
        #     if w != '':
        #         res2_tokens.append(w)
        # res2 = ' '.join(res2_tokens)
        #
        # res2findall = res_lang.findall(res1.strip())
        # resultdict['lang'] = res2findall
        # details.append("【{}】6==>【{}】".format(res1, res2))
        #
        # # 4. 预判断:is in tag_dict or not
        # c_tag = []
        # if len(res2_tokens) == 1:
        #     if res2 in self.tag_dict.keys():
        #         c_tag = [res2]
        # else:
        #     for tok in res2_tokens:
        #         if tok in self.tag_dict.keys():
        #             if res2 in self.tag_dict[tok].keys():
        #                 c_tag = [res2]
        #             else:
        #                 continue
        #
        # if len(c_tag) >= 1:
        #     resultdict["lang"] = c_tag
        #     details.append("【{}】7==>【{}】".format(res1, c_tag))
        #     self.log.debug("Clean {} type tag details:{}".format("lang", details))
        #     return c_tag, resultdict, details
        # else:
        #     pass
        #
        # # 小于2元词不处理,直接返回
        # if len(res1_tokens) < 2:
        #     resultdict["lang"] = [res2]
        #     details.append("【{}】8==>【{}】".format(new_tag, res2))
        #     self.log.debug("Clean {} type tag details:{}".format("lang", details))
        #     return [res2], resultdict, details
        # else:
        #     pass
        # return [res2], resultdict, details



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



    def standard_tag(self, raw_tag):
        # print(">>>>> 正在标准化tag")
        standard_tag_list1 = ["new", "game", "sport", "highlight", "idol", "kb", "goal", "vlog",
                              "play", "interview", "transfer", "song", "recipe", "champion", "tutorial", "skill",
                              "giant", "dog", "battleground", "legend", "kid", "animal", "final", "fichaje", "cat", "movie",
                              "toy", "tip", "spur", "creator", "star", "fruit", "girl", "playoff", "gooner", "prank",
                              "deporte", "video", "assist", "noticia", "youtuber", "cosmetic", "dribble", "blue", "replay", "puma",
                              "mark", "dunk", "exercise", "hairstyle", "voice", "review", "celebration", "cartoon",
                              "american"]

        standard_tag_list2 = ["k-pop", "v-log", "k-food", "g-20", "make-up", "e-sports", "k-drama", "a-pink",
                              "min-a", "k-beauty", "hip-hop", "a-jax", "k-culture", "k-popcover", "k-star",
                              "uh-oh", "play-offs", "hyun-jin", "la-liga", "t-series", "wan-bissaka", "u-20",
                              "jin-young", "hyun-moo", "so-mi", "hyeong-don", "k-style", "ji-won", "jong-shin",
                              "gyu-ri", "k-뷰티", "j-hope", "ji-eun", "min-ho", "young-jae", "u-know", "u-kiss",
                              "gu-ra", "ji-hye", "seul-gi", "ju-ne", "jung-kook", "c-clown", "j-reyez", "ga-in",
                              "sung-min", "block-b", "new-tro", "eun-i", "g-dragon", "hyun-a", "g-idle",
                              "chung-ha", "wo-man", "4-4-2oons", "monsta-x", "jae-seok", "seung-yoon", "dong-yup",
                              "ac-milan", "hat-trick", "real-madrid", "c-jes", "b-boy", "슈퍼주니어-d&e", "ha-neul",
                              "twi-light", "a-teen", "ph-1", "k-ville", "ji-hyo", "line-up", "chae-young", "i-dle",
                              "yeon-jung", "manchester-united", "xo-iq", "tteok-bokki", "hye-won", "woo-sung",
                              "do-yeon", "k-9", "u-15", "semi-finals", "sung-jae", "seung-hoon", "na-young",
                              "transfer-news", "heung-min", "j-pop", "premier-league", "u-20월드컵", "jin-hwan",
                              "so-yi", "sae-rom", "jin-woo"]

        for tag in standard_tag_list1:
            if raw_tag.find(tag + ' ') >= 0 or raw_tag.find(" " + tag) >= 0 or raw_tag == tag:
                if raw_tag.find(tag + 's ') >= 0 or raw_tag.find(" " + tag + "s") >= 0 or raw_tag == tag + "s":
                    raw_tag = raw_tag
                else:
                    raw_tag = raw_tag.replace(tag, tag + "s")
            else:
                continue
        for tag in standard_tag_list2:
            if raw_tag.find(tag.replace("-", "") + " ") >= 0 or raw_tag.find(
                    " " + tag.replace("-", "")) >= 0 or raw_tag == tag.replace("-", ""):
                raw_tag = raw_tag.replace(tag.replace("-", ""), tag)
            elif raw_tag.find(tag.replace("-", " ") + " ") >= 0 or raw_tag.find(
                    " " + tag.replace("-", " ")) >= 0 or raw_tag == tag.replace("-", " "):
                raw_tag = raw_tag.replace(tag.replace("-", " "), tag)
            else:
                continue
        tag_tok = raw_tag.split(" ")
        if len(tag_tok) == 1:
            standardtag_list = [k + "s" for k in standard_tag_list1] + standard_tag_list2
            for tag in standardtag_list:
                if raw_tag.find(tag):
                    raw_tag = raw_tag.replace(tag, tag + " ")
                else:
                    continue

        return raw_tag

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

    def pre_clean(self, text):
        """
        预处理文本
        1.剔除全数字（match日期）
        2.剔除带‘=’的字符
        3.替换带括号的字符,替换‘#’字符
        :param text:
        :return:
        """
        details = list()
        result_tag = dict()
        tag = ""
        l_tag = text.lower()
        symbol_text, symbol_detail = self.remove_symbol(l_tag)
        details.append("【{}】0==>【{}】".format(l_tag, symbol_text))
        result_tag['symbol'] = symbol_text

        return symbol_text

    @staticmethod
    def remove_symbol(text):
        """
        清除符号
        :param text:
        :return:
        """
        sym_patten = re.compile(r"\(.*?\)|#", flags=0)
        if text.find("=") < 0:
            non_sym = sym_patten.sub("", text)
            detail = "non_symbol_tag"
            new_tag = non_sym.strip()
        else:
            detail = "non_symbol_tag"
            new_tag = ""
        return new_tag, detail

    @staticmethod
    def detect_lang(text):
        """
        检测非韩语、非英语外的tag
        :param text:
        :return:
        """
        detail = ''
        try:
            lang = langdetect.detect(text)
        except:
            lang = 'none'
        finally:
            if lang not in ['ko', 'en']:
                detail = 'non_ko_en_tag'
                return "", detail
            else:
                detail = 'ko_or_en_tag'
                return text, detail


    def rm_num(self, text):
        """
        清除纯数字，年份、日期标记
        :param text:
        :return:
        """
        detail = ''

        try:
            float(text)
            detail = 'num_tag'
            return "", detail
        except:
            if text.isdigit():
                time_str = self.clean_period(text)
                if time_str:
                    detail = 'time_tag'
                    return time_str, detail
                else:
                    detail = 'num_tag'
                    return time_str, detail
            else:
                return text, detail

