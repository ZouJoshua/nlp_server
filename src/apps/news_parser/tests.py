from django.test import TestCase

# Create your tests here.

from unittest import main, TestCase

from .parser_processer.get_html import HtmlDownloader
from .parser_processer.parse_html import HtmlPaser
from .parser_processer.user_agents import user_agent_list

import sys
sys.path.append("/home/zoushuai/algoproject/nlp_parser_server/src")
sys.path.append("/home/zoushuai/algoproject/nlp_parser_server/src/web")

from config.n_parser_conf import PARSER_DATA_PATH

import random
import time
import os
import json



class TestPredict(TestCase):
    # id = "1502889409622478"
    title = "2 kids die in different incidents"
    content = """Erode, Aug 16 (PTI) A three-year-old child died in a road accident, while a 11-month-old was electrocuted while playing in his house at suburban Karungalpalayam in two different incidents in the district, police said. they said the 3-year-old male child died on the spot when he was thrown off after a college van rammed the motorcycle he was travelling with his parents from the rear at Bhavani Both the husband and wife were seriously injured and have been hospitalised. In the second incident late last night,the 11 month child accidentally came in contact with a live wire, attached to the television. The parents rushed him to a private nursing home from where he was referred to Government Headquarters Hospital late last night, but the toddler died, police said. This is published unedited from the PTI feed."""
    url = "http://www.deccanchronicle.com/entertainment/bollywood/180818/the-jonas-clan-is-here.html"

    @classmethod
    def setUpClass(cls):
        print(">>>>>>>>>>测试环境已准备好！")
        print(">>>>>>>>>>即将测试 Case ...")

    @classmethod
    def tearDownClass(cls):
        print(">>>>>>>>>>Case 用例已测试完成 ...")
        print(">>>>>>>>>>测试环境已清理完成！")

    def test_spider(self):
        s = time.time()
        hd = HtmlDownloader()
        header = self.get_http_header()
        html = hd.download(self.url, header)
        s1 = time.time()
        print(">>>>>>>>>>请求网页耗时： {}".format(s1 - s))

    def test_parser(self):
        s = time.time()
        hd = HtmlDownloader()
        header = self.get_http_header()
        html = hd.download(self.url, header)
        s1 = time.time()
        print(">>>>>>>>>>请求网页耗时： {}".format(s1 - s))
        rules_xpath, new_domains_file, xpath_error_file = self.get_file()
        hp = HtmlPaser(new_domains_fo=new_domains_file, xpath_error_fo=xpath_error_file)
        result = hp.parse(self.url, html, rules_xpath)
        s2 = time.time()
        print(">>>>>>>>>>解析网页耗时： {}".format(s2 - s1))

    def get_file(self):
        NLP_PARSER_FILE_PATH = os.path.join(PARSER_DATA_PATH, 'rule.json')
        with open(NLP_PARSER_FILE_PATH, 'r', encoding='utf-8') as jf:
            rules_xpath = json.load(jf)
        NEW_DOMAINS_FILE = os.path.join(PARSER_DATA_PATH, 'new_domain.txt')
        XPATH_ERROR_FILE = os.path.join(PARSER_DATA_PATH, 'xpath_error.txt')
        new_domains_file = open(NEW_DOMAINS_FILE, "a+")
        xpath_error_file = open(XPATH_ERROR_FILE, "a+")
        return rules_xpath, new_domains_file, xpath_error_file

    def get_http_header(self):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': random.choice(user_agent_list)['User-Agent']
        }



if __name__ == '__main__':
    main()