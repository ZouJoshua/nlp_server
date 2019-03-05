#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/5 16:36
@File    : run.py
@Desc    : 
"""

import subprocess
import os
import sys
import time

HOME = os.getcwd()
SCRPET = os.path.basename(sys.argv[0])
if len(sys.argv) != 4 or sys.argv[1] == '-h':
    sys.exit("Usage:sudo %s ServerName {Port} {start, stop, restart}" % SCRPET)

RUN = "python3"
NAME = sys.argv[1]
PORT = sys.argv[2]
OP = sys.argv[3]

DAEMON = '-d'
NAME_NOPOSTFIX = NAME.split(".")[0]
PIDFILE = "{}/.{}_pidfile".format(HOME, NAME_NOPOSTFIX)
# if DEPLOY == 'prod':
#     HOME_DIRS = HOME.split('/')
#     crawler_index = HOME_DIRS.index('vertical_crawler')
#     if HOME_DIRS[crawler_index + 1].find('_') != -1:
#         port_offset = HOME_DIRS[crawler_index + 1].split('_')[1]
#     else:
#         port_offset = '1'
#     LOG_DIR = '/data/logs/python/' + HOME_DIRS[crawler_index] + '/' + HOME_DIRS[crawler_index + 1]
#     LN_LOG_DIR = HOME + '/log'
#     if not os.path.exists(LOG_DIR):
#         os.makedirs(LOG_DIR)
#     try:
#         os.symlink(LOG_DIR, LN_LOG_DIR)
#     except Exception as e:
#         print(str(e))
# else:
#     port_offset = '1'
#     LOG_DIR = HOME + '/log'
#     if not os.path.exists(LOG_DIR):
#         os.makedirs(LOG_DIR)


def start():
    print(" | ".join([HOME, NAME]))
    print("Starting {} ...".format(NAME))
    if os.path.exists(PIDFILE):
        print("{} has been running | PID:{}\nContinue?(Y/N)".format(NAME, open(PIDFILE).readline()))
        k = input()
        if not k in ("Y", "y"):
            sys.exit(1)
    try:
        p = subprocess.Popen([RUN, 'manage.py', 'runserver', PORT], stdout=subprocess.PIPE)
        # p = subprocess.Popen('ls')
        # ���������־
        # out = p.stdout.read()
        # open(LOGFILE, "a").write(out)
        time.sleep(3)
        # pid = p.pid
        pid = open(PIDFILE).readline()
        # open(PIDFILE, "w").write("%s" % pid)
        print(" | ".join(["Start OK", "PID:%s" % pid]))
    except Exception as e:
        print(e)


def stop():
    if not os.path.exists(PIDFILE):
        return
    pid = open(PIDFILE).readline()
    print("Stopping", NAME, '...')
    if pid:
        if subprocess.call(["kill -15 " + pid], shell=True) == 0:
            print(" | ".join(["Stop OK", "PID:%s" % pid]))
        if subprocess.call(["rm " + PIDFILE], shell=True) != 0:
            print("Delete Permission Denied")
    else:
        print("Stop Error")


def restart():
    stop()
    time.sleep(1)
    start()


ops = {"start": start, "stop": stop, "restart": restart}

if __name__ == "__main__":
    ops[OP]()