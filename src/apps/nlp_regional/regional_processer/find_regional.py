#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/29 20:00
@File    : find_regional.py
@Desc    : 
"""

import re
import threading
import time
import os


class Find(threading.Thread):
    def __init__(self, namelist, startIndex, endIndex, text, finddict):
        threading.Thread.__init__(self)
        self.namelist = namelist  # 要搜索的数据的内存地址
        self.startIndex = startIndex  # 开始的索引
        self.endIndex = endIndex  # 结束的索引
        self.seachstr = text
        self.finddict = finddict

    def run(self):
        self._finddict = dict()
        for i in range(self.startIndex, self.endIndex):
            findone = re.findall(self.namelist[i] + '[\W]', self.seachstr)
            if len(findone):
                self._finddict[self.namelist[i].strip()] = len(findone)
        global mutex  # 多线程共享全局变量(全局锁)
        global finddict
        with mutex:  # 获取锁(自动释放锁)
            self.finddict.update(self._finddict)
