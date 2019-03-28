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
import logging

class LoadRegionalMap(object):

    def __init__(self, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("load_regional_map")

    def load_regional_map(self, path):
        """
        用于加载模型和分类ID的映射关系
        :param path: path为本地模型所在文件夹路径 
        :return: 模型列表（dict）、分类ID的映射（json）
        """
        pass