#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-9 上午11:16
@File    : get_html.py
@Desc    : 
"""

import requests
from requests.exceptions import Timeout, HTTPError
import logging

# 从网站中抓取数据

class HtmlDownloader(object):

    def __init__(self, logger=None):
        self.TIMEOUT = 5
        self.RETRY_TIME = 1
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("nlp_parser")
    # @staticmethod
    def download(self,url, header):
        try:
            response = requests.get(url=url, headers=header, timeout=self.TIMEOUT)
            html = response.text
        except Timeout as e:
            self.log.error("Download html {} error {}".format(url, e))
            html = 'timeout'
        except HTTPError as e:
            self.log.error("Download html {} error {}".format(url, e))
            html = "Others error"
        except Exception:
            count = 0  # 重试次数
            while count < self.RETRY_TIME:
                count += 1
                try:
                    self.log.info("Retry requests {} the {} time".format(url, count))
                    response = requests.get(url=url, headers=header, timeout=self.TIMEOUT)
                    html = response.text
                except Exception as _e:
                    self.log.error("Retry download html {} error {}".format(url, _e))
        return html