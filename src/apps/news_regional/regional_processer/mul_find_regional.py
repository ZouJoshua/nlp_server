#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/29 20:00
@File    : mul_find_regional.py
@Desc    : 
"""

import re
import threading
import time
import os


class Find(threading.Thread):
    def __init__(self, namelist, startIndex, endIndex, text):
        threading.Thread.__init__(self)
        self.namelist = namelist  # 要搜索的数据的内存地址
        self.startIndex = startIndex  # 开始的索引
        self.endIndex = endIndex  # 结束的索引
        self.seachstr = text

    def run(self):
        self._finddict = dict()
        for i in range(self.startIndex, self.endIndex):
            findone = re.findall(self.namelist[i] + '[\W]', self.seachstr)
            if len(findone):
                self._finddict[self.namelist[i].strip()] = len(findone)
        FINDREGIONALDICT.update(self._finddict)
        # global finddict  # 多线程共享全局变量(全局锁)
        # if lock.acquire():
        #     # 获取锁(自动释放锁)
        #     try:
        #         finddict.update(self._finddict)
        #     finally:
        #         lock.release()


def multithread_find_regional(text, names_map, thread_num=30):
    global lock, FINDREGIONALDICT
    FINDREGIONALDICT = dict()
    namelist = list(names_map.keys())
    namenum = len(namelist)
    print(namenum)
    # lock = threading.Lock()# 创建一个锁
    threadlist = []  # 线程列表
    # 97 9    0-1000000  1000000-2000000  2000000-3000000
    for i in range(0, thread_num - 1):
        mythd = Find(namelist, i * (namenum // (thread_num - 1)), (i + 1) * (namenum // (thread_num - 1)), text)
        mythd.start()
        threadlist.append(mythd)  # 添加到线程列表
    # 97 =  97//10*10=90
    mylastthd = Find(namelist, namenum // (thread_num - 1) * (thread_num - 1), namenum, text)  # 最后的线程搜索剩下的尾数
    mylastthd.start()
    threadlist.append(mylastthd)  # 添加到线程列表
    for thd in threadlist:  # 遍历线程列表
        thd.join()
    return FINDREGIONALDICT