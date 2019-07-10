#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-6-28 下午4:17
@File    : load_mapdata.py
@Desc    : 
"""

import json


class LoadDict(object):

    def __init__(self, en_vtags_file, en_tag2type_file, es_type_tags,es_base_tags,stopwords_file):
        self.en_vtag2kwline = dict()
        self.en_kw2vtag = dict()
        self.en_fix2list = dict()
        self.en_word2fix = dict()
        self.stopwords = dict()
        self.es_base_tags = list()
        self.es_type_tags = dict()
        self.load_en_dict(en_vtags_file, en_tag2type_file, stopwords_file)
        self.load_es_dict(es_type_tags, es_base_tags)

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
            standard_tag_dict = json.load(es_standard_tag_file)

        self.es_base_tags = list(standard_tag_dict.keys())




if __name__ == "__main__":
    ld = LoadDict('./dict1/vtags.0413', './dict1/trim2', './dict1/stopwords.txt')