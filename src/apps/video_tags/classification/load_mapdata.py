#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-6-28 下午4:17
@File    : load_mapdata.py
@Desc    : 
"""


class LoadDict(object):

    def __init__(self, vtags_file, tag2type_file, stopwords_file):
        self.vtag2kwline = dict()
        self.kw2vtag = dict()
        self.fix2list = dict()
        self.word2fix = dict()
        self.stopwords = dict()
        self.load_dict(vtags_file, tag2type_file, stopwords_file)

    def load_dict(self, vtags_file, tag2type_file, stopwords_file):
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
                        if word not in self.kw2vtag:
                            self.kw2vtag[word] = set()
                        self.kw2vtag[word].add(vtag)
                self.vtag2kwline[vtag] = [n_grame, ','.join(kwtoken), df, flag, deleteflag]

        with open(tag2type_file, 'r') as f1:
            for line in f1:
                tokens = line.strip().split('\t')
                if len(tokens) < 2: continue
                fix = tokens[0]
                original_wordlist = [x.split(':')[0] for x in tokens[1].split(',')]
                self.fix2list[fix] = original_wordlist

        for fix, original_wordlist in self.fix2list.items():
            for w in original_wordlist:
                w2 = w.replace(fix, '').strip()
                if w2 in self.fix2list:
                    self.word2fix[w] = w2
                else:
                    self.word2fix[w] = fix
        with open(stopwords_file, 'r') as f2:
            for line in f2:
                line = line.strip()
                self.stopwords[line] = None


if __name__ == "__main__":

    load_dict('./dict1/vtags.0413', './dict1/trim2', './dict1/stopwords.txt')