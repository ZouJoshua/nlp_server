#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/29 20:00
@File    : find_regional.py
@Desc    : 
"""

import threading, time


def countstr(f):
    global findstr, occurtimes
    times = 0
    for string in f:
        if findstr in string:
            times += 1
    occurtimes.append(times)


occurtimes = []
threadnum = int(input("please input thread number:"))
filename = input("please input filename:")
findstr = input("please input to find string:")
text = open(filename).readlines()
start = time.time()
threads = []
for i in range(threadnum):
    t = threading.Thread(target=countstr, args=(text[i::threadnum],))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
end = time.time()
print("multithread using %.5f seocnds" % (end - start))
print('string "%s" occurs %d times' % (findstr, sum(occurtimes)))
print
occurtimes = []
start = time.time()
countstr(text)
end = time.time()
print("singlethread uing %.5f seconds" % (end - start))
print('string "%s" occurs %d times' % (findstr, sum(occurtimes)))

import threading
import os


class Find(threading.Thread):  # 搜索数据的线程类
    def __init__(self, datalist, startIndex, endIndex, searchstr,
                 savefile):  # datalist要搜索的内容列表，startIndex列表搜索范围的开始下标，searchstr要搜索的内容
        threading.Thread.__init__(self)
        self.datalist = datalist  # 要搜索的数据的内存地址
        self.startIndex = startIndex  # 开始的索引
        self.endIndex = endIndex  # 结束的索引
        self.seachstr = searchstr  # 需要搜索的数据
        self.savefile = savefile

    def run(self):
        self.findlist = []
        for i in range(self.startIndex, self.endIndex):
            line = self.datalist[i].decode("gbk", "ignore")  # 读取一行
            if line.find(self.seachstr) != -1:
                print(self.getName(), line, end="")  # 搜索数据
                self.findlist.append(line)
        global mutex  # 多线程共享全局变量(全局锁)
        with mutex:  # 获取锁(自动释放锁)
            for line in self.findlist:
                self.savefile.write(line.encode("gbk"))


mutex = threading.Lock()  # 创建一个锁
savefile = open("c:\\zhaodao.txt", "wb")  # 搜索到的内容写入该文件

path = "C:\\data1.txt"  # 要搜索的文件
file = open(path, "rb")
datalist = file.readlines()  # 全部读入内存
lines = len(datalist)  # 所有的行数
searchstr = input("输入要查询的数据")
N = 10  # 开启10个线程
threadlist = []  # 线程列表
# 97 9    0-1000000  1000000-2000000  2000000-3000000
for i in range(0, N - 1):  # 0,1,2,3,4,5,6,7,8  数据切割
    mythd = Find(datalist, i * (lines // (N - 1)), (i + 1) * (lines // (N - 1)), searchstr, savefile)  # //表示整除
    mythd.start()
    threadlist.append(mythd)  # 添加到线程列表

# 97 =  97//10*10=90
mylastthd = Find(datalist, lines // (N - 1) * (N - 1), lines, searchstr, savefile)  # 最后的线程搜索剩下的尾数
mylastthd.start()
threadlist.append(mylastthd)  # 添加到线程列表

for thd in threadlist:  # 遍历线程列表
    thd.join()
print("finish")
