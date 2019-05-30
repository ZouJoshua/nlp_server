#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-5-30 上午10:40
@File    : taste_client.py
@Desc    : 新闻浏览口味分类客户端请求
"""

import requests

url1 = 'http://127.0.0.1:16601/nlp_category/taste'


title = "Messenger App Gets New Powerful Camera"
content = """To help make conversations better, Facebook on Friday launched a new, faster and easier-to-use camera with art and special effects in its Messenger app that will be rolled out globally over the coming days. “We have seen that the way people are messaging is becoming much more visual. In fact, over 2.5 billion emojis, photos, stickers and videos are sent every day on Messenger,” the company said in a blog. “In some ways the camera is now replacing the keyboard. As more people use Messenger in their everyday lives, we wanted to make it faster, simpler and more fun to send photos and videos. So we built the new Messenger camera,” Facebook said. The new camera is quicker than previous versions which makes it easier for users to capture and share moments as they happen. Whether you are already in a conversation or have just opened up the app, you will see the shutter button centre in the screen. A tap takes photo and a long press records a video. The social media giant also introduced new art and special effects. “We are especially excited to debut 3D masks and special effects, which make it super easy to apply an artistic filter to your full screen photo and to turn your world into a work of art,” the company said. Facebook has also incorporated thousands of stickers, frames, masks and effects in the app. A user can also create text, add art and stickers to the text. """
_id = "1000"


# 请求
"""
传入参数：
    id: string(必传)
    title: string（必传）
    content: string（必传）
    thresholds: float（可不传，默认参数0.3）
"""
parms = {"id": _id, "title": title, "content": content, "thresholds": 0.3}

# category test
resp1 = requests.post(url1, data=parms)  # 发送请求
# Decoded text returned by the request
print(resp1.text)