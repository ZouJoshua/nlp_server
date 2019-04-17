#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-17 上午11:12
@File    : crawl_handler.py
@Desc    : 
"""


import threading
import time



class CrawlHandler(threading.Thread):

    def __init__(self):
        '''
        Constructor
        '''
        super(CrawlHandler, self).__init__()
    def SetupQueue(self, input_, output_):
        self.input_queue = input_
        self.output_queue = output_
    def OutputQueueSize(self):
        if self.output_queue:
            return self.output_queue.qsize()
        return 0
    def WaitForOutputReady(self):
        kMaxOutputQueueSize = 3000
        while self.OutputQueueSize() > kMaxOutputQueueSize:
            time.sleep(1)
    def HandleOneCrawlTask(self, task):
        pass
    def Output(self, task):
        if not self.output_queue:
            return
        self.WaitForOutputReady()
        self.output_queue.put(task)
    def run(self):
        if not self.input_queue:
            return
        while True:
            while not self.input_queue.empty():
                task = self.input_queue.get()
                self.HandleOneCrawlTask(task)
                self.Output(task)
                while self.input_queue.empty():
                    time.sleep(0.5)




