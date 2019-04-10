#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-9 下午2:05
@File    : parse_html.py
@Desc    : 
"""

import logging
from urllib.parse import urlparse
from lxml.html import etree
import json
import sys

class HtmlPaser(object):

    def __init__(self, logger=None, new_domains_fo=None, xpath_error_fo=None):
        """
        初始化两个队列及日志
        :param logger:
        :param new_domains_queue: 新域名队列
        :param xpath_error_queue: xpath解析错误队列
        """
        self.new_file = new_domains_fo
        self.error_file = xpath_error_fo
        if logger:
            self.log = logger
        else:
            self.log = logging.getLogger("nlp_parser")

    def parse(self, url, html, rules_xpath):
        domain = urlparse(url).netloc
        result = {"category": [], "title": [], "tag": [], "hyperlink_text": [], "hyperlink_url": []}
        _keys = ["category", "title", "tag", "hyperlink_text", "hyperlink_url"]
        if domain in rules_xpath.keys():
            for key in _keys:
                xp = rules_xpath.get(domain).get(key)
                if xp != 'none':
                    try:
                        pt = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
                        _j = pt.xpath(xp)
                        if len(_j) > 0:
                            result[key] = [n.strip().strip("\n\t") for n in _j]
                    except Exception as _e:
                        self.log.error("Parse html {} error {}".format(url, _e))
                        # self.error_queue.put({url: key})
                        self.error_file.write(json.dumps({url: key}) + "\n")
                        sys.stdout.flush()
                        self.error_file.flush()

            self.log.info("Successful parse html {},\nresult:{}".format(url, result))
        else:
            self.log.warning("Dose not exist xpath of {}".format(domain))
            # self.new_queue.put(domain)
            self.new_file.write(json.dumps({domain: url}) + "\n")
            sys.stdout.flush()
            self.new_file.flush()

        return result