#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-5-10 上午10:40
@File    : v_category_client.py
@Desc    : 视频分类客户端请求
"""

import requests

url1 = 'http://127.0.0.1:15501/nlp_category/video_cat'

title = "GRADUATION MAKEUP TUTORIAL"
content = """Wanna see more BeautyBeautyGuru24? LIKE this video and COMMENT \"More\"\n\nSUBSCRIBE FOR MORE: http://tinyurl.com/n9jxdvz\n\nFollow My Social-ness\nTWITTER: \nhttps://twitter.com/Machaizelli\nINSTAGRAM: \nhttp://instagram.com/macdoesit\nTUMBLR: \nhttp://macdoesit.tumblr.com/\nFACEBOOK\nhttp://facebook.com/MacDoesIt\n\n----------------------------\n\nElectric Joy Ride - Origin: https://www.youtube.com/watch?v=iScT5IfgG-Q\n\nFollow Electric Joy Ride:\nhttp://www.facebook.com/ElectricJoyRide\nhttps://soundcloud.com/electricjoyride\nhttp://www.youtube.com/user/ElectricJ...\nhttp://twitter.com/ElectricJoyRide\n\n\nDavid Bulla - Highlife: https://www.youtube.com/watch?v=5H4XVwnrmo4\n\nDavid Bulla:\nListen https://soundcloud.com/davidbullaoffical\nFollow https://twitter.com/itsdavidbulla\nSubscribe http://www.youtube.com/user/EnergyyMusiC\nLike http://www.facebook.com/davidbullaoff... \nWebsite davidbulla.de/"""
_id = "1000"
tag_list = "machaizelli, funny, vlog, MacDoesIt, graduation makeup, makeup, garduation look, tutorial, michelle phan, parody, beauty guru, college, university, school, graduation song, vitamin c graduation, high school graduation, escape from school"

# 请求
"""
传入参数：
    newsid: string(必传)
    title: string（必传）
    content: string（必传）
    tag_list: string（必传）
"""
parms = {"newsid": _id, "title": title, "content": content, "tag_list": tag_list}

# category test
resp1 = requests.post(url1, data=parms)  # 发送请求
# Decoded text returned by the request
print(resp1.text)