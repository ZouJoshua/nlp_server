#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/4 10:26
@File    : load_regional_map.py
@Desc    : 
"""

import json
import os
import re
import logging
from web.settings import NLP_REGIONAL_DATA_PATH


class LoadRegionalMap(object):

    def __init__(self, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("nlp_regional_predict")

    def load_regional_map(self, path):
        """
        用于加载地域名称映射关系
        :param path: path为地域数据文件夹路径
        :return: 地域映射（json）
        """
        if not os.path.exists(path):
            bak_file = os.path.join(NLP_REGIONAL_DATA_PATH, 'india_names2regions_bak.json')
            if not os.path.exists(bak_file):
                self.log.warning('No bak file {} exists'.format('india_names2regions_bak.json'))
                self._regional_preprocess()
        with open(path, 'r', encoding='utf-8') as reader:
            names_map = json.load(reader)
        return names_map

    def _regional_preprocess(self):
        filename = 'india_division.json'
        regi_file = os.path.join(NLP_REGIONAL_DATA_PATH, filename)
        if not os.path.exists(regi_file):
            self.log.error('No file {} exists'.format(filename))
            raise Exception('No file {} exists'.format(filename))
        result = self._process_regional(regi_file)
        regi2map_file = os.path.join(NLP_REGIONAL_DATA_PATH, 'india_names2regions.json')
        with open(regi2map_file, 'w') as f:
            json.dump(result, f, indent=4)
        return

    def _process_regional(self, regi_file):
        reader = open(regi_file, 'r', encoding='utf-8')
        line = json.load(reader)
        out = dict()
        # print(line)
        for k, v in line.items():
            if k in ['States', 'Union territories']:
                states = line[k]
                for _k, _v in states.items():
                    out_result = {"regional": '',
                                  'is_capital': False, 'is_regions': False,
                                  'is_divisions': False, 'is_districts': False,
                                  'is_headquarters': False, 'is_largest_city': False,
                                  'is_sub_districts': False, 'is_town': False}
                    if _k not in out.keys():
                        out_result['regional'] = _k
                        out[_k] = out_result
                    for i, j in _v.items():
                        if j:
                            if i == 'districts_new':
                                i = 'districts'
                                j_upper = list()
                                for d in j:
                                    j_upper.append(d.title().replace("District", "").strip().upper())
                                j += j_upper
                            elif i == 'capital' or i == 'headquarters':
                                j_upper = list()
                                for d in j:
                                    j_upper.append(d.title().strip().upper())
                                j += j_upper
                            for _j in j:
                                if _j not in out.keys():
                                    out_result = {"regional": '',
                                                  'is_capital': False, 'is_regions': False,
                                                  'is_divisions': False, 'is_districts': False,
                                                  'is_headquarters': False, 'is_largest_city': False,
                                                  'is_sub_districts': False, 'is_town': False}
                                    out_result['regional'] = _k
                                    out_result['is_{}'.format(i)] = True
                                    _j_clean = re.sub('\s+', ' ',
                                                      _j.replace("*", " ").replace("District", "").replace("Division",
                                                                                                           "").strip())
                                    out[_j_clean] = out_result
                                else:
                                    out_result = out[_j]
                                    out_result['regional'] = _k
                                    out_result['is_{}'.format(i)] = True
                                    _j_clean = re.sub('\s+', ' ',
                                                      _j.replace("*", " ").replace("District", "").replace("Division",
                                                                                                           "").strip())
                                    out[_j_clean] = out_result
                        else:
                            continue
        reader.close()
        return out