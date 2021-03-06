#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-6-28 下午4:17
@File    : load_mapdata.py
@Desc    : 
"""

import json
import os
import logging
from config.video_tags_conf import PROJECT_LOG_FILE, NLP_MODEL_PATH
from .en_vtag_process import EnProcess
from .es_vtag_process import EsProcess
from .ko_vtag_process import KoProcess
from .de_vtag_process import DeProcess
from .pt_vtag_process import PtProcess
from .ru_vtag_process import RuProcess
from .ja_vtag_process import JaProcess
from .normal_vtag_process import NormalProcess



class LoadMultiCountryTagInstance(object):
    # en_vtags_file = os.path.join(NLP_MODEL_PATH, 'en_vtags.0413')
    # en_trim_file = os.path.join(NLP_MODEL_PATH, 'en_base_tags')
    # stopwords_file = os.path.join(NLP_MODEL_PATH, 'stopwords.txt')
    # es_base_tag_file = os.path.join(NLP_MODEL_PATH, 'es_base_tags')
    # es_type_tag_file = os.path.join(NLP_MODEL_PATH, 'es_type_tags')
    # ko_base_tag_file = os.path.join(NLP_MODEL_PATH, 'ko_base_tags')
    # ko_type_tag_file = os.path.join(NLP_MODEL_PATH, 'ko_type_tags')
    # de_base_tag_file = os.path.join(NLP_MODEL_PATH, 'de_base_tags')
    # de_type_tag_file = os.path.join(NLP_MODEL_PATH, 'de_type_tags')

    def __init__(self, lang_list, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("vtag_process")
            self.log.setLevel(logging.INFO)
        self.log.info("Initialization start...")
        self.log.info("Loading multi country tag file...")
        self.lang_list = lang_list
        ld = LoadDict(NLP_MODEL_PATH, self.lang_list, logger=self.log)
        self.en_vtag2kwline = ld.en_vtag2kwline
        self.en_fix2list = ld.en_fix2list
        self.en_word2fix = ld.en_word2fix
        self.en_kw2vtag = ld.en_kw2vtag
        self.multi_lang_dict = ld.multi_lang_dict
        self.stopwords = ld.stopwords

        self.log.info("Successfully cache tag infomations of multi country")

    def load_process_instance(self):
        multi_lang_instance_dict = dict()

        for lang in self.lang_list:
            if lang == 'en':
                en_proc = EnProcess(self.en_vtag2kwline, self.en_fix2list, self.en_word2fix,
                                    self.en_kw2vtag, self.stopwords, logger=self.log)
                self.log.info("Successfully load en tag process instance...")
                multi_lang_instance_dict["en_instance"] = en_proc
            else:
                type_tag = "{}_type_tags".format(lang)
                base_tag = "{}_base_tags".format(lang)
                if type_tag in self.multi_lang_dict and base_tag in self.multi_lang_dict:
                    type_tags = self.multi_lang_dict[type_tag]
                    base_tags = self.multi_lang_dict[base_tag]
                    if lang == 'es':
                        es_proc = EsProcess(type_tags, base_tags, self.stopwords, logger=self.log)
                        multi_lang_instance_dict["es_instance"] = es_proc
                        self.log.info("Successfully load es tag process instance...")
                    elif lang == 'ko':
                        ko_proc = KoProcess(type_tags, base_tags, self.stopwords, logger=self.log)
                        multi_lang_instance_dict["ko_instance"] = ko_proc
                        self.log.info("Successfully load ko tag process instance...")
                    elif lang == 'de':
                        de_proc = DeProcess(type_tags, base_tags, self.stopwords, logger=self.log)
                        multi_lang_instance_dict["de_instance"] = de_proc
                        self.log.info("Successfully load de tag process instance...")
                    elif lang == 'pt':
                        pt_proc = PtProcess(type_tags, base_tags, self.stopwords, logger=self.log)
                        multi_lang_instance_dict["pt_instance"] = pt_proc
                        self.log.info("Successfully load pt tag process instance...")
                    elif lang == 'ru':
                        ru_proc = RuProcess(type_tags, base_tags, self.stopwords, logger=self.log)
                        multi_lang_instance_dict["ru_instance"] = ru_proc
                        self.log.info("Successfully load ru tag process instance...")
                    elif lang == 'ja':
                        ja_proc = JaProcess(type_tags, base_tags, self.stopwords, logger=self.log)
                        multi_lang_instance_dict["ja_instance"] = ja_proc
                        self.log.info("Successfully load ja tag process instance...")
                    else:
                        self.log.warning("Processing of language {} is not supported".format(lang))
                else:
                    self.log.warning("{} or {} not found".format(type_tag, base_tag))
        normal_proc = NormalProcess(logger=self.log)
        multi_lang_instance_dict["normal_instance"] = normal_proc
        self.log.info("Successfully load normal tag process instance...")
        self.log.debug("multi_lang_instance_dict: {}".format(multi_lang_instance_dict.keys()))
        return multi_lang_instance_dict



class LoadDict(object):

    def __init__(self,
                 data_dir, lang_list,
                 logger=None):
        self.en_vtag2kwline = dict()
        self.en_kw2vtag = dict()
        self.en_fix2list = dict()
        self.en_word2fix = dict()
        self.stopwords = dict()
        self.data_dir = data_dir
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("vtag_process")
            self.log.setLevel(logging.INFO)
        self.lang_list = lang_list
        # self.load_en_dict(en_vtags_file, en_tag2type_file, stopwords_file)
        self.multi_lang_dict = self.load_multi_lang_dict()
        # self.load_es_dict(es_type_tags, es_base_tags)
        # self.load_ko_dict(ko_type_tags, ko_base_tags)
        # self.load_de_dict(de_type_tags, de_base_tags)

    def load_en_dict(self, vtags_file, tag2type_file, stopwords_file):
        with open(vtags_file, 'r') as f0:
            for line in f0:
                tokens = line.strip().split('\t')
                if len(tokens) < 6: continue
                vtag = tokens[0]
                n_grame = int(tokens[1])
                kwline = tokens[2]
                df = int(tokens[3])
                flag = int(tokens[4])
                deleteflag = int(tokens[5])
                if deleteflag != 0: continue
                kwtoken = []
                for word in kwline.split(','):
                    word = word.strip()
                    if word != '' and word != vtag:
                        kwtoken.append(word)
                        if word not in self.en_kw2vtag:
                            self.en_kw2vtag[word] = set()
                        self.en_kw2vtag[word].add(vtag)
                self.en_vtag2kwline[vtag] = [n_grame, ','.join(kwtoken), df, flag, deleteflag]

        with open(tag2type_file, 'r') as f1:
            for line in f1:
                tokens = line.strip().split('\t')
                if len(tokens) < 2: continue
                fix = tokens[0]
                original_wordlist = [x.split(':')[0] for x in tokens[1].split(',')]
                self.en_fix2list[fix] = original_wordlist

        for fix, original_wordlist in self.en_fix2list.items():
            for w in original_wordlist:
                w2 = w.replace(fix, '').strip()
                if w2 in self.en_fix2list:
                    self.en_word2fix[w] = w2
                else:
                    self.en_word2fix[w] = fix
        with open(stopwords_file, 'r') as f2:
            for line in f2:
                line = line.strip()
                self.stopwords[line] = None

    def load_multi_lang_dict(self):

        multi_lang_dict = dict()
        for lang in self.lang_list:
            if lang == 'en':
                en_vtags_file = os.path.join(self.data_dir, 'en_vtags.0413')
                if not os.path.exists(en_vtags_file):
                    self.log.error("Type file {} of {} not found".format(en_vtags_file, lang))
                    raise Exception("Type file {} of {} not found".format(en_vtags_file, lang))
                en_tag2type_file = os.path.join(self.data_dir, 'en_base_tags')
                if not os.path.exists(en_tag2type_file):
                    self.log.error("Base file {} of {} not found".format(en_tag2type_file, lang))
                    raise Exception("Base file {} of {} not found".format(en_tag2type_file, lang))
                stopwords_file = os.path.join(self.data_dir, 'stopwords.txt')
                if not os.path.exists(stopwords_file):
                    self.log.error("Stopwords file {} of {} not found".format(stopwords_file, lang))
                    raise Exception("Stopwords file {} of {} not found".format(stopwords_file, lang))
                self.load_en_dict(en_vtags_file, en_tag2type_file, stopwords_file)
            else:
                type_tag_file = os.path.join(self.data_dir, "{}_type_tags".format(lang))
                if os.path.exists(type_tag_file):
                    with open(type_tag_file, 'r') as f:
                        tag_dict = json.load(f)
                    multi_lang_dict["{}_type_tags".format(lang)] = tag_dict
                else:
                    self.log.error("Type file {} of {} not found".format(type_tag_file, lang))
                    raise Exception("Type file {} of {} not found".format(type_tag_file, lang))
                base_tag_file = os.path.join(self.data_dir, "{}_base_tags".format(lang))
                if os.path.exists(base_tag_file):
                    with open(base_tag_file, 'r') as f:
                        standard_tag_dict = json.load(f)
                    multi_lang_dict["{}_base_tags".format(lang)] = list(standard_tag_dict.keys())
                else:
                    self.log.error("Base file {} of {} not found".format(base_tag_file, lang))
                    raise Exception("Base file {} of {} not found".format(base_tag_file, lang))

        self.log.debug("multi_lang_dict: {}".format(multi_lang_dict.keys()))

        return multi_lang_dict


    # def load_es_dict(self, es_type_file, es_standard_tag_file):
    #
    #     with open(es_type_file, 'r') as f:
    #         tag_dict = json.load(f)
    #     self.es_type_tags = tag_dict
    #
    #     with open(es_standard_tag_file, 'r') as f:
    #         standard_tag_dict = json.load(f)
    #
    #     self.es_base_tags = list(standard_tag_dict.keys())
    #
    #
    # def load_ko_dict(self, ko_type_file, ko_standard_tag_file):
    #
    #     with open(ko_type_file, 'r') as f:
    #         tag_dict = json.load(f)
    #     self.ko_type_tags = tag_dict
    #
    #     with open(ko_standard_tag_file, 'r') as f:
    #         standard_tag_dict = json.load(f)
    #
    #     self.ko_base_tags = list(standard_tag_dict.keys())
    #
    # def load_de_dict(self, de_type_file, de_standard_tag_file):
    #
    #     with open(de_type_file, 'r') as f:
    #         tag_dict = json.load(f)
    #     self.de_type_tags = tag_dict
    #
    #     with open(de_standard_tag_file, 'r') as f:
    #         standard_tag_dict = json.load(f)
    #
    #     self.de_base_tags = list(standard_tag_dict.keys())

