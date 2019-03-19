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


url1 = 'http://10.65.0.76:19901/nlp_category/category'
url2 = 'http://10.65.0.76:19901/nlp_category/top'
url3 = 'http://10.65.0.76:19901/nlp_category/sub'


title = "Messenger App Gets New Powerful Camera"
content = """To help make conversations better, Facebook on Friday launched a new, faster and easier-to-use camera with art and special effects in its Messenger app that will be rolled out globally over the coming days. “We have seen that the way people are messaging is becoming much more visual. In fact, over 2.5 billion emojis, photos, stickers and videos are sent every day on Messenger,” the company said in a blog. “In some ways the camera is now replacing the keyboard. As more people use Messenger in their everyday lives, we wanted to make it faster, simpler and more fun to send photos and videos. So we built the new Messenger camera,” Facebook said. The new camera is quicker than previous versions which makes it easier for users to capture and share moments as they happen. Whether you are already in a conversation or have just opened up the app, you will see the shutter button centre in the screen. A tap takes photo and a long press records a video. The social media giant also introduced new art and special effects. “We are especially excited to debut 3D masks and special effects, which make it super easy to apply an artistic filter to your full screen photo and to turn your world into a work of art,” the company said. Facebook has also incorporated thousands of stickers, frames, masks and effects in the app. A user can also create text, add art and stickers to the text. """
top_category = "technology"
parms = {"title": title, "content": content, "top_category": top_category}


# category test
resp1 = requests.post(url1, data=parms)  # 发送请求
# Decoded text returned by the request
print(resp1.text)

# top_category test
resp2 = requests.post(url2, data=parms)  # 发送请求
# Decoded text returned by the request
print(resp2.text)

# sub_category test
resp3 = requests.post(url3, data=parms)  # 发送请求
# Decoded text returned by the request
print(resp3.text)

