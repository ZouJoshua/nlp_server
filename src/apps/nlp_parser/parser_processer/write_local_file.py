#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 19-4-9 下午4:20
@File    : write_local_file.py
@Desc    : 启动多进程处理写文件
"""

import time
import random
import json
import sys
from multiprocessing import Pool, Manager


def write_file(file, queue, log):
    log.info("Start writing file {}".format(file))
    with open(file, 'a+') as f:

        while True:
            if not queue.empty():
                value = queue.get(False)
                log.info("Get {} from queue {}".format(value, queue))
                f.write(json.dumps(value) + "\n")
                sys.stdout.flush()
                f.flush()
                # time.sleep(random.random())
            else:
                break

