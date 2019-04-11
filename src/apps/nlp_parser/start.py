#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-9 下午6:57
@File    : start.py
@Desc    : 
"""

from .parser_processer.get_html import HtmlDownloader
from .parser_processer.parse_html import HtmlPaser
from utils.logger import Logger
from web.settings import PROJECT_LOG_FILE, PROJECT_DATA_PATH

from .parser_processer.write_local_file import write_file
from multiprocessing import Pool, Manager

import os
import json


def init_start():
    logger = Logger('nlp_parser', log2console=False, log2file=True, logfile=PROJECT_LOG_FILE).get_logger()
    logger.info("Initialization start...")
    logger.info("Loading xpath rule file...")
    NLP_EN_PARSER_FILE_PATH = os.path.join(PROJECT_DATA_PATH, 'rules.json')
    with open(NLP_EN_PARSER_FILE_PATH, 'r', encoding='utf-8') as jf:
        rules_xpath = json.load(jf)
    # manager = Manager()
    # # 父进程创建Queue，并传给各个子进程：
    # out_q1 = manager.Queue()
    # out_q2 = manager.Queue()
    NEW_DOMAINS_FILE = os.path.join(PROJECT_DATA_PATH, 'new_domain.txt')
    XPATH_ERROR_FILE = os.path.join(PROJECT_DATA_PATH, 'xpath_error.txt')
    new_domains_file = open(NEW_DOMAINS_FILE, "a+")
    xpath_error_file = open(XPATH_ERROR_FILE, "a+")
    hd = HtmlDownloader(logger=logger)
    hp = HtmlPaser(logger=logger, new_domains_fo=new_domains_file, xpath_error_fo=xpath_error_file)

    # p = Pool()
    # nd_q = p.apply_async(write_file, args=(NEW_DOMAINS_FILE, out_q1, logger))
    # xe_q = p.apply_async(write_file, args=(XPATH_ERROR_FILE, out_q2, logger))
    # p.close()
    # p.join()
    return rules_xpath, hd, hp, logger