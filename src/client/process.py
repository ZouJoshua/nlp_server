#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-17 下午12:06
@File    : process.py
@Desc    : 
"""



import random
import json
import os
import sys
from urllib.parse import urlparse
import requests

import threading
import queue as Queue
import time

base_path = os.path.dirname((os.path.dirname(os.path.realpath(__file__))))
sys.path.append(base_path)
sys.path.append(os.path.join(base_path, 'web'))
from web.settings import PROJECT_LOG_FILE, PROJECT_DATA_PATH

url = 'http://127.0.0.1:8020/nlp_parser/parser'

data_file = '/data/zoushuai/news_content/html/dt=2019-04-11/url_random'
# data_file = "/data/in_hi_html_random.json"

NLP_PARSER_FILE_PATH = os.path.join(PROJECT_DATA_PATH, 'rules.json')



def produce_task_queue(data_file, left, right):
    task_queue = Queue.Queue()
    new_task_queue = Queue.Queue()
    with open(NLP_PARSER_FILE_PATH, 'r', encoding='utf-8') as jf:
        rules_xpath = json.load(jf)
    _of = open(data_file, 'r')
    lines = _of.readlines()[left:right]
    for _line in lines:
        line = json.loads(_line.strip())
        _url = line['url']
        _id = line['id']
        domain = urlparse(_url).netloc
        if domain in rules_xpath['hi'].keys():
            print(_id)
            task_queue.put(line)
        else:
            new_task_queue.put(line)
    task_queue.put('None')
    new_task_queue.put('None')
    _of.close()
    print(task_queue.qsize())
    print(new_task_queue.qsize())
    return task_queue, new_task_queue

class SpiderParserHandler(threading.Thread):

    def __init__(self, task_queue, result_queue):
        self._tq = task_queue
        self._rq = result_queue
        super(SpiderParserHandler, self).__init__()

    def run(self):
        global existFlag, lock
        while not existFlag:
            if self._tq.empty():
                break
            lock.acquire()
            data = self._tq.get()
            # self._tq.task_done()
            lock.release()
            if data != 'None':
                _url = data['url']
                _id = data['id']
                parms = {'id': _id, 'website': _url, "lang": "hi"}
                resp = requests.post(url, data=parms)
                result = {'id': _id, 'url': _url, 'result': resp}
                self._rq.put(result)
            else:
                time.sleep(1)
                self._rq.put('None')
                break


class ResultHandler(threading.Thread):

    def __init__(self, data_queue, localfile, task_type=None):
        self.data_queue = data_queue
        self.localfile = localfile
        self.tt = task_type
        self.nu = {"category": [], "title": [], "tag": [], "hyperlink_text": [], "hyperlink_url": []}
        super(ResultHandler, self).__init__()

    def _dataprocess(self, data):
        '''Get data from queue'''
        _url = data['url']
        _id = data['id']
        if not self.tt:
            resp = data['result']
            if resp.status_code != 408:
                out = {str(_id): json.loads(resp.text), "url": _url}
            else:
                out = {str(_id): self.nu, "url": _url}
        else:
            out = {str(_id): _url}
        return out

    def run(self):
        global existFlag, filelock
        _of = open(self.localfile, "w")
        while not existFlag:
            data = self.data_queue.get()
            # self.data_queue.task_done()
            if data != 'None':
                # print(data)
                out = self._dataprocess(data)
                _of.write(json.dumps(out) + '\n')
                sys.stdout.flush()
                _of.flush()
                # filelock.release()
            else:
                if self.data_queue.empty():
                    print("任务结束")
                    # filelock.release()
                    _of.close()
                    # self.data_queue.task_done()
                    break


def write_file_from_queue(localfile, data_queue):
    _of = open(localfile, "w")
    while not existFlag:
        data = data_queue.get()
        if data != 'None':
            _url = data['url']
            _id = data['id']
            out = {str(_id): _url}
            _of.write(json.dumps(out) + '\n')
            sys.stdout.flush()
            _of.flush()
        else:
            if data_queue.empty():
                print("新域名写入文件已完成")
                _of.close()
                break



def start():
    global existFlag, lock, filelock
    existFlag = 0
    _WORKER_THREAD_NUM = 10
    threads = []
    result_q = Queue.Queue()
    task_q, new_task_q = produce_task_queue(data_file, 400000, 1000000)
    time.sleep(3)
    task_result_file = '/data/zoushuai/hi_news_parser_20190418'
    new_task_result_file = '/data/zoushuai/hi_news_new_domain_20190418'

    # task_result_file = '/home/zoushuai/algoproject/nlp_parser_server/src/data/test/result20190418'
    # new_task_result_file = '/home/zoushuai/algoproject/nlp_parser_server/src/data/test/new_domain_task'

    write_file_from_queue(new_task_result_file, new_task_q)

    for i in range(_WORKER_THREAD_NUM):
        thread = SpiderParserHandler(task_q, result_q)
        thread.start()
        threads.append(thread)
    time.sleep(3)
    write_task_thread = ResultHandler(result_q, task_result_file)

    write_task_thread.start()
    threads.append(write_task_thread)
    time.sleep(1)

    for thread in threads:
        thread.join()



if __name__ =='__main__':
    lock = threading.Lock()
    filelock = threading.Lock()
    start()