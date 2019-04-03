#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/29 17:15
@File    : predict.py
@Desc    : 
"""

import re
import logging
from .mul_find_regional import multithread_find_regional
import threading


class Predict(object):

    def __init__(self, regional_map=None, logger=None):
        self.reg_map = regional_map
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("nlp_regional_predict")
            self.log.setLevel(logging.INFO)


    def get_regional(self, content='', title=''):
        text = content + '.' + title
        out_count = self.get_detail_regional(text, self.reg_map)
        regional_ct = self. _count_regional(out_count, self.reg_map)

        return self._get_regional(regional_ct, text)

    def get_regional_multithread(self, content='', title=''):
        text = content + '.' + title
        out_count = self._find_regional_multithread(text, self.reg_map)
        regional_ct = self._count_regional(out_count, self.reg_map)

        return self._get_regional(regional_ct, text)


    def _get_regional(self, regional_ct, text, topk=3):
        regional = dict()
        regional['regional'] = list()
        if regional_ct:
            ks = regional_ct.keys()
            deh = ['National Capital Territory Of Delhi', 'Delhi']
            dehil_names = set(deh) & set(ks)
            city = ['Mumbai', 'Bengaluru', 'Kolkata', 'Hyderabad']
            city_names = set(city) & set(ks)
            if dehil_names:
                if re.findall('New Delhi:', text) or re.findall('Delhi:', text) or re.findall('DELHI:', text):
                    regional['regional'].append('Delhi')
                else:
                    if len(dehil_names) == 2:
                        if regional_ct['Delhi'] >= regional_ct['National Capital Territory Of Delhi']:
                            del regional_ct['National Capital Territory Of Delhi']
                        else:
                            del regional_ct['Delhi']
            elif city_names:
                for city in city_names:
                    _city = city + ':'
                    if re.findall(_city, text) or re.findall(_city.upper(), text):
                        regional['regional'].append(city)
            if not regional['regional']:
                sort_regional_ct = sorted(regional_ct.items(), key=lambda x: x[1], reverse=True)
                topk_regional_ct = sort_regional_ct[:topk]
                if len(topk_regional_ct) == 1:
                    regional['regional'].append(topk_regional_ct[0][0])
                elif len(topk_regional_ct) > 1:
                    if topk_regional_ct[0][1] > topk_regional_ct[1][1]:
                        regional['regional'].append(topk_regional_ct[0][0])
                    elif topk_regional_ct[0][1] == topk_regional_ct[1][1]:
                        regional['regional'].append(topk_regional_ct[0][0])
                        # regional['regional'].append(topk_regional_ct[1][0])
                        # if len(topk_regional_ct) > 2 and topk_regional_ct[1][1] == topk_regional_ct[2][1]:
                        #     regional['regional'].append(topk_regional_ct[2][0])
                        # else:
                        #     pass
                self.log.info('Get the region of the article {}'.format(regional))
        result = dict()
        result['regional'] = ''
        if len(regional['regional']):
            result['regional'] = regional['regional'][0]
        return result

    def get_detail_regional(self, text, names_map):
        out = dict()
        for key, value in names_map.items():
            # if len(key) < 5:
            #     key += ' '
            all = re.findall(key + '[\W]', text)
            if len(all):
                out[key.strip()] = len(all)
        self.log.info('Get all the regional names of the article\n{}'.format(out))
        return self._re_count_regional(out)

    def _find_regional_multithread(self, text, names_map):
        finddict = multithread_find_regional(text, names_map)
        self.log.info('Get all the regional names of the article\n{}'.format(finddict))
        return self._re_count_regional(finddict)

    def _re_count_regional(self, regional_ct):
        out = dict()
        if regional_ct:
            for k, v in regional_ct.items():
                if k.isupper():
                    k = k.title()
                if k not in out:
                    out[k] = v
                else:
                    out[k] += v
        self.log.info('Standardize all regional names\n{}'.format(out))
        return out

    def _count_regional(self, result, names_map):
        out = dict()
        for k, v in result.items():
            if k in ['Mumbai', 'Bengaluru', 'Kolkata', 'Hyderabad']:
                region = k
            else:
                region = names_map[k]['regional']
            if region not in out:
                out[region] = v
            else:
                out[region] += v
        self.log.info('Get state and city statistics\n{}'.format(out))
        return out
