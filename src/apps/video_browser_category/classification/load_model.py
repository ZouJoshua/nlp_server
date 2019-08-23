#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-8-22 下午4:31
@File    : load_model.py
@Desc    : 加载模型及label映射
"""


import fasttext
import json
import os
import logging



class LoadModel(object):

    def __init__(self, logger=None):

        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("load_classification_model")

    def load_models_and_idmap(self, path):
        """
        用于加载模型和分类ID的映射关系
        :param path: path为本地模型所在文件夹路径
        :return: 模型列表（dict）、分类ID的映射（json）
        """
        classifier_dict = dict()
        # 加载一级模型
        topcategory_model_path = os.path.join(path, 'browser_category_model.bin')
        topcategory_sub_model_path = os.path.join(path, 'browser_category_sub_model.bin')
        if os.path.exists(topcategory_model_path) and os.path.exists(topcategory_sub_model_path):
            topcategory_classifier = fasttext.load_model(topcategory_model_path)
            classifier_dict['topcategory_model'] = topcategory_classifier
            sub_classifier = fasttext.load_model(topcategory_sub_model_path)
            classifier_dict['topcategory_sub_model'] = sub_classifier
            self.log.info('Successfully loaded the first-level classification model')
        elif os.path.exists(topcategory_model_path):
            topcategory_classifier = fasttext.load_model(topcategory_model_path)
            classifier_dict['topcategory_model'] = topcategory_classifier
            self.log.warning('Successfully loaded the first-level classification model without sub_model')
        else:
            self.log.error('Please check if the first-level model path exists')
            raise Exception('一级分类模型路径不存在')

        # 加载分类id映射表
        idx2labelmap_path = os.path.join(path, "idx2label_map.json")
        if os.path.exists(idx2labelmap_path):
            with open(idx2labelmap_path, "r") as load_f:
                idx2label_map = json.load(load_f)
            self.log.info('Successfully loaded classification id mapping')
        else:
            self.log.error('Please check if the classification id mapping exists')
            raise Exception('分类id映射路径不存在')

        return classifier_dict, idx2label_map