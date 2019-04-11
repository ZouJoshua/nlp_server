#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/2/28 18:41
@File    : client.py
@Desc    : 客户端
"""

import requests
import json

url1 = 'http://127.0.0.1:10901/nlp_category/category'
url2 = 'http://127.0.0.1:10901/nlp_category/top'
url3 = 'http://127.0.0.1:10901/nlp_category/sub'


id = "1502776564471413"
title = "Independence Day 2017: These freedom fighters studied in foreign universities"
content = """We have heard and read how our freedom fighters fought bravely for an independent India. Most of these nationalists were well-educated and their education ignited their self-esteem to fight for the country’s freedom. Few of them got the chance to acquire knowledge from the reputed foreign universities. They used innovative methods like the boycott of foreign goods to rebel against the British empire. We bring to you a list of these nationalists who went to foreign universities. Mahatma Gandhi The ‘Father of the nation,’ Mahatma Gandhi shook the British empire with his non-violent protests. Born in Gujarat, he studied law at University College London and returned to India to work as a barrister. Dr BR Ambedkar Dr Bhimrao Ramji Ambedkar fought for equality for all, especially for the underprivileged. He was also a noted economist and lawyer. His keen interest in law, economics and political science made him secure multiple degrees from various Indian and foreign universities. He did PhD from the Columbia University and MSc from the London School of Economics. He also went to the University of Bonn in Germany to study economics. Jawaharlal Nehru Jawaharlal Nehru was India’s first Prime Minister who studied at Harrow which is one of England’s leading schools. He then completed his graduation with an honours degree in natural science in 1910. He later went to the Inner Temple where he trained to be a barrister at law. He found a mentor in Mahatama Gandhi and together they worked for an independent India. Varahagiri Venkata Giri Born on August 10, 1894 in Berhampore, Venkata Giri or VV Giri was the son of noted advocate and freedom fighter, Jogayya Panthulu. His early education was at the Kallikote College, Berhampur. He went to Dublin in 1913 to study law. Sarojini Naidu Sarojini Naidu was a bright student and daughter of principal of the Nizam’s College, Hyderabad. She got a scholarship and she entered the University of Madras at the age of 12 and studied (1895–98) at King’s College, London, and later at Girton College, Cambridge. For all the latest Education News, download Indian Express App"""
top_category = 'national'

parms = {"id": id, "title": title, "content": content, "top_category": top_category}

## >>>>>>>>>> 请求一级和二级类参数
"""
传入参数：
    title: string（必传）
    content: string（必传）
    thresholds: （float，float）（可不传，默认参数（0.3,0.2））
"""
# category test
resp1 = requests.post(url1, data=parms)  # 发送请求
print(resp1.text)

## >>>>>>>>>> 单独请求一级类参数
"""
传入参数：
    title: string（必传）
    content: string（必传）
    thresholds: float（可不传，默认参数0.3）
"""
# parms = {"title": title, "content": content, "thresholds": 0.3}

# top_category test
# resp2 = requests.post(url2, data=parms)  # 发送请求
# print(resp2.text)

## >>>>>>>>>> 单独请求二级类参数
"""
传入参数：
    title: string（必传）
    content: string（必传）
    top_category: string（必传）
    thresholds: float（可不传，默认参数0.2）
"""
# parms = {"title": title, "content": content, "top_category": top_category, "thresholds": 0.2}

# sub_category test
# resp3 = requests.post(url3, data=parms)  # 发送请求
# print(resp3.text)
