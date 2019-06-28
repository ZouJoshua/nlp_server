#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-5-10 上午10:40
@File    : v_category_client.py
@Desc    : 视频分类客户端请求
"""

import requests

url1 = 'http://127.0.0.1:9022/polls/vtag'


title = "Actress Bhavana Latest Images | Tollywood Updates"
content = """To help make conversations better, Facebook on Friday launched a new, faster and easier-to-use camera with art and special effects in its Messenger app that will be rolled out globally over the coming days. “We have seen that the way people are messaging is becoming much more visual. In fact, over 2.5 billion emojis, photos, stickers and videos are sent every day on Messenger,” the company said in a blog. “In some ways the camera is now replacing the keyboard. As more people use Messenger in their everyday lives, we wanted to make it faster, simpler and more fun to send photos and videos. So we built the new Messenger camera,” Facebook said. The new camera is quicker than previous versions which makes it easier for users to capture and share moments as they happen. Whether you are already in a conversation or have just opened up the app, you will see the shutter button centre in the screen. A tap takes photo and a long press records a video. The social media giant also introduced new art and special effects. “We are especially excited to debut 3D masks and special effects, which make it super easy to apply an artistic filter to your full screen photo and to turn your world into a work of art,” the company said. Facebook has also incorporated thousands of stickers, frames, masks and effects in the app. A user can also create text, add art and stickers to the text. """
_id = "1000"
category = "214"
vtaglist = "actress bhavana rare and unseen family pics,atest celebrity updates,total tollywood,bhava,actress bhavana,bhavana family,bhavana family pics,bhavana family images,bhavana family photos,actress bhavana family pics,actress bhavana friends,celebrity family photos,celebrity news,celebrity updates,latest celebrity news,latest celebrity updates,Actress Bhavana Latest Images"
resource_type = "1"
business_type = "0"

# 请求
"""
传入参数：
    newsid: string(必传)
    title: string（必传）
    vtaglist: string（必传）
    content: string（必传）
    category: string()
    sub_category: string()
    resource_type: string(0：文章 1：视频)
    business_type: string(0:浏览器 1:游戏)
"""
parms = {"newsid": _id, "title": title, "vtaglist": vtaglist, "content": content, "category": category, "business_type":business_type,"resource_type":resource_type}

# category test
resp1 = requests.post(url1, data=parms)  # 发送请求
# Decoded text returned by the request
print(resp1.text)