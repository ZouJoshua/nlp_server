#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/5/30 10:26
@File    : load_model.py
@Desc    : 
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
        category_model_path = os.path.join(path, 'taste_classification_model.bin')
        if os.path.exists(category_model_path):
            clf = fasttext.load_model(category_model_path)
            self.log.info('Successfully loaded the taste classification model')
        else:
            self.log.error('Please check if the model path exists')
            raise Exception('浏览口味分类模型路径不存在')
        # 加载分类id映射表
        idx2labelmap_path = os.path.join(path, "idx2label_map.json")
        if os.path.exists(idx2labelmap_path):
            with open(idx2labelmap_path, "r") as load_f:
                idx2label = json.load(load_f)
            if "tastecategory" in idx2label.keys():
                idx2label_map = idx2label["tastecategory"]
            else:
                idx2label_map = {"0": "泛娱乐", "1": "新闻", "2": "专业", "3": "其他"}
            self.log.info('Successfully loaded classification id mapping')
        else:
            self.log.error('Please check if the classification id mapping exists')
            raise Exception('分类id映射路径不存在')

        return clf, idx2label_map


    # 结果
    # classifier_dict = {"topcategory_model":model,
    #                    "auto_science":model,
    #                   "international":model,
    #                    ...}
    # idx2label_map = {
    #     "topcategory":{
    #     "3": "international",
    #     "4": "national",
    #     "6": "sports",
    #     ...
    #     },
    # "subcategory":{
    #     "401":"crime",
    #     "402":"education",
    #     ...
    #     }
    # }