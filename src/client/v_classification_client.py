#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-9-10 上午10:40
@File    : v_category_client.py
@Desc    : 视频分类(tensorflow)客户端请求
"""

import requests

url1 = 'http://127.0.0.1:17001/nlp_category/video_cats'

_id = "1000"
v_url = "/home/zoushuai/Downloads/videoplayback.mp4"

# 请求
"""
传入参数：
    video_id: string(必传)
    video_url: string（必传）
"""
parms = {"video_id": _id, "video_url": v_url}

# category test
resp1 = requests.post(url1, data=parms)  # 发送请求
# Decoded text returned by the request
print(resp1.text)