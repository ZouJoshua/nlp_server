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
from src.utils.daemonize import *


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
server_name = os.path.split(os.path.realpath(sys.argv[1]))[-1].replace('.py', '')
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
        p.wait()
        if PORT:
            daemonize('./.nlp_server_pidfile')
        while not os.path.exists(PIDFILE):
            time.sleep(0.1)
        pid = open(PIDFILE).readline().strip()
        # p = subprocess.Popen('ls')
        # ���������־
        # out = p.stdout.read()
        time.sleep(3)
        # pid = p.pid
        print(" | ".join(["Start OK", "PID:%s" % pid]))
        open(PIDFILE, 'a').write('%d\n' % os.getpid())
    except Exception as e:
        print(e)

    return pid


def stop():
    if not os.path.exists(PIDFILE):
        return
    pid_list = open(PIDFILE).readlines()
    pid = None
    monitor_pid = None
    if len(pid_list) == 1:
        pid = pid_list[0].strip()
    elif len(pid_list) == 2:
        pid = pid_list[0].strip()
        monitor_pid = pid_list[1].strip()
    else:
        print(NAME, " Stop error")
        return

    print("Stopping", NAME, '...')
    if monitor_pid:
        if subprocess.call(["kill -15 " + monitor_pid], shell=True) == 0:
            time.sleep(0.2)
            pass
        else:
            print(NAME, " monitor stop error")
    else:
        pass

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
    return start()


ops = {"start": start, "stop": stop, "restart": restart}

if __name__ == "__main__":
    pid = ops[OP]()
    if OP == 'start' \
            or OP == 'restart':
        while True:
            cmd = 'ps -ef | grep %s | grep -v "grep" | ' \
                  'grep %s | awk \'{print $2}\'' % (pid, server_name)
            ps_pid = os.popen(cmd).read().strip()
            # print 'ps_pid,pid', ps_pid,pid
            if ps_pid != pid:
                # pass
                subprocess.call(["rm " + PIDFILE], shell=True)
                pid = ops['start']()
            else:
                pass
            time.sleep(1)