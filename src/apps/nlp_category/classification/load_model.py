#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/4 10:26
@File    : load_model.py
@Desc    : 
"""

import fasttext
import json
import os
import logging

class LoadModel(object):

    def __init__(self, logger=None):
        self.topcategory_list = ["international", "national", "sports", "technology", "business", "science", "auto", "lifestyle",
                        "entertainment"]
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
        topcategory_model_path = os.path.join(path, 'top_content_model.bin')
        topcategory_auto_science_model_path = os.path.join(path, 'top_auto_science_model.bin')
        if os.path.exists(topcategory_model_path) and os.path.exists(topcategory_auto_science_model_path):
            topcategory_classifier = fasttext.load_model(topcategory_model_path)
            classifier_dict['topcategory_model'] = topcategory_classifier
            auto_science_classifier = fasttext.load_model(topcategory_auto_science_model_path)
            classifier_dict['auto_science'] = auto_science_classifier
            self.log.info('Successfully loaded the first-level classification model')
        else:
            self.log.error('Please check if the first-level model path exists')
            raise Exception('一级分类模型路径不存在')
        # 加载二级模型
        for topcategory in self.topcategory_list:
            model_path = os.path.join(path, "{}_sub_classification_model.bin".format(topcategory))
            if os.path.exists(model_path):
                classifier = fasttext.load_model(model_path)
                classifier_dict[topcategory] = classifier
                self.log.info('Successfully loaded secondary classification model \n{}'.format(model_path))
            self.log.warning('The secondary classification model ({}) does not exist and the loading fails'.format(model_path))
            continue
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