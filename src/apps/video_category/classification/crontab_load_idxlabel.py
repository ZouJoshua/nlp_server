#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-5-7 上午11:00
@File    : crontab_load_idxlabel.py
@Desc    : 定时加载映射表
"""

from django.core.cache import cache

import json
import requests
import logging
import os
import sys
apps_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(apps_dir), 'config'))
from config.video_category_conf import NLP_MODEL_PATH



logger = logging.getLogger("nlp_v_category_predict")
# NLP_MODEL_PATH = '/home/zoushuai/algoproject/nlp_v_category_server/src/data'

def crontab_load(r_type="1", b_type="0"):

    """
    :return: IDX2LABEL_MAP
    """
    file = os.path.join(NLP_MODEL_PATH, 'idx2label.json')
    lim = LoadIdxMap(logger=logger)
    idx = lim.load_update_idx2label(file, r_type, b_type)
    # cache.set("IDX2LABEL_MAP", idx)
    return idx


class LoadIdxMap(object):

    def __init__(self, logger=None):
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("load_classification_model")
            self.log.setLevel(logging.INFO)

    def load_update_idx2label(self, file, r_type, b_type):
        idx2label_file = self.load_idx2label_from_file(file)
        idx2label_requests = self.get_category_dict_from_requests(r_type, b_type)
        if idx2label_file == idx2label_requests:
            return idx2label_file
        else:
            new_file = os.path.join(NLP_MODEL_PATH, 'idx2label_new.json')
            with open(new_file, 'w') as nf:
                nf.writelines(json.dumps(idx2label_requests, indent=4))
            return idx2label_requests

    def load_idx2label_from_file(self, file):
        # idx2label = self.get_category_dict_from_requests(r_type="1", b_type="0")
        # with open(file, 'w') as nf:
        #     nf.writelines(json.dumps(idx2label, indent=4))
        with open(file, 'r') as f:
            idx = json.load(f)
        return idx


    def get_category_dict_from_requests(self, r_type, b_type):
        url = "http://cms-news-api.apuscn.com/classify/getList/{}".format(r_type)
        try:
            response = requests.get(url)
        except Exception as e:
            self.log.error("Request classification interface api error")
            idx2label = dict()
        else:
            requests_data = response.text
            idx2label = self._deal_with_response(requests_data, b_type)
        return idx2label

    def _deal_with_response(self, requests_data, b_type):

        r_data = json.loads(requests_data)
        idx2label = dict()
        for i in r_data['data']:
            # if i["bizType"] == int(b_type):
            idx2label[i['classifyId']] = {
                "top_category": [{"id": i["classifyId"], "category": i["classifyName"], "proba": 1.0}],
                "sub_category": [{"id": -1, "category": "", "proba": 0.0}]}
            if i["children"]:
                for j in i["children"]:
                    value = {"top_category": [
                        {"id": i["classifyId"], "category": i["classifyName"], "proba": 1.0}],
                        "sub_category": [
                            {"id": j["classifyId"], "category": j["classifyName"],
                             "proba": 1.0}]}
                    if "other" in j["classifyName"].lower():
                        key = "{}({})".format(i["classifyId"], "-1")
                        idx2label[j["classifyId"]] = value
                        idx2label[key] = value
                    else:
                        key = j["classifyId"]
                        idx2label[key] = value
            # else:
            #     self.log.warning("Discover other classification business types: {}".format(i["bizType"]))
        return idx2label


# file = "/home/zoushuai/algoproject/nlp_v_category_server/src/data/idx2label.json"
# s = LoadIdxMap()
# s.load_idx2label_from_file(file)