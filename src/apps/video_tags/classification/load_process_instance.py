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
from .normal_vtag_process import NormalProcess



class LoadMultiCountryTagInstance(object):
    en_vtags_file = os.path.join(NLP_MODEL_PATH, 'en_vtags.0413')
    en_trim_file = os.path.join(NLP_MODEL_PATH, 'en_base_tags')
    stopwords_file = os.path.join(NLP_MODEL_PATH, 'stopwords.txt')
    es_base_tag_file = os.path.join(NLP_MODEL_PATH, 'es_base_tags')
    es_type_tag_file = os.path.join(NLP_MODEL_PATH, 'es_type_tags')
    ko_base_tag_file = os.path.join(NLP_MODEL_PATH, 'ko_base_tags')
    ko_type_tag_file = os.path.join(NLP_MODEL_PATH, 'ko_type_tags')

    def __init__(self, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("vtag_process")
            self.log.setLevel(logging.INFO)
        self.log.info("Initialization start...")
        self.log.info("Loading multi country tag file...")

        ld = LoadDict(self.en_vtags_file, self.en_trim_file,
                      self.es_type_tag_file, self.es_base_tag_file,
                      self.ko_type_tag_file, self.ko_base_tag_file,
                      self.stopwords_file)
        self.en_vtag2kwline = ld.en_vtag2kwline
        self.en_fix2list = ld.en_fix2list
        self.en_word2fix = ld.en_word2fix
        self.en_kw2vtag = ld.en_kw2vtag
        self.es_base_tags = ld.es_base_tags
        self.es_type_tags = ld.es_type_tags
        self.ko_base_tags = ld.ko_base_tags
        self.ko_type_tags = ld.ko_type_tags
        self.stopwords = ld.stopwords

        self.log.info("Successfully cache tag infomations of multi country")

    def load_process_instance(self):
        en_proc = EnProcess(self.en_vtag2kwline, self.en_fix2list, self.en_word2fix,
                            self.en_kw2vtag, self.stopwords, logger=self.log)
        self.log.info("Successfully load en tag process instance...")

        es_proc = EsProcess(self.es_type_tags, self.es_base_tags, self.stopwords, logger=self.log)
        self.log.info("Successfully load es tag process instance...")

        ko_proc = KoProcess(self.ko_type_tags, self.ko_base_tags, self.stopwords, logger=self.log)
        self.log.info("Successfully load ko tag process instance...")

        normal_proc = NormalProcess(logger=self.log)
        self.log.info("Successfully load normal tag process instance...")



        return en_proc, es_proc, ko_proc, normal_proc



class LoadDict(object):

    def __init__(self,
                 en_vtags_file, en_tag2type_file,
                 es_type_tags, es_base_tags,
                 ko_type_tags, ko_base_tags,
                 stopwords_file):
        self.en_vtag2kwline = dict()
        self.en_kw2vtag = dict()
        self.en_fix2list = dict()
        self.en_word2fix = dict()
        self.stopwords = dict()
        self.es_base_tags = list()
        self.es_type_tags = dict()
        self.load_en_dict(en_vtags_file, en_tag2type_file, stopwords_file)
        self.load_es_dict(es_type_tags, es_base_tags)
        self.load_ko_dict(ko_type_tags, ko_base_tags)

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


    def load_es_dict(self, es_type_file, es_standard_tag_file):

        with open(es_type_file, 'r') as f:
            tag_dict = json.load(f)
        self.es_type_tags = tag_dict

        with open(es_standard_tag_file, 'r') as f:
            standard_tag_dict = json.load(f)

        self.es_base_tags = list(standard_tag_dict.keys())


    def load_ko_dict(self, ko_type_file, ko_standard_tag_file):

        with open(ko_type_file, 'r') as f:
            tag_dict = json.load(f)
        self.ko_type_tags = tag_dict

        with open(ko_standard_tag_file, 'r') as f:
            standard_tag_dict = json.load(f)

        self.ko_base_tags = list(standard_tag_dict.keys())

