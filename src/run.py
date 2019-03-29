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
from utils.daemonize import daemonize


HOME = os.getcwd()
SCRPET = os.path.basename(sys.argv[0])
if len(sys.argv) != 4 or sys.argv[1] == '-h':
    sys.exit("Usage:sudo %s {ServerName} {start, stop, restart}" % SCRPET)

RUN = "python3"
SERVER_NAME = sys.argv[1]
NAME = sys.argv[2]
OP = sys.argv[3]

# server ip
SERVER_HOSTS = os.environ.get('SERVER_HOSTS', '127.0.0.1')
SERVER_PORT = os.environ.get('PORT', 10901)

SERVER_NAME_PIDFILE = '.{}_pidfile'.format(SERVER_NAME)
PIDFILE = "{}/{}".format(HOME, SERVER_NAME_PIDFILE)
cmd_server_name = os.path.split(os.path.realpath(NAME))[-1].replace('.py', '')


def start():
    print(" | ".join([HOME, NAME]))
    print("Starting {} ...".format(SERVER_NAME))
    if os.path.exists(PIDFILE):
        print("{} has been running | PID:{}\nContinue?(Y/N)".format(SERVER_NAME, open(PIDFILE).readline()))
        k = input()
        if not k in ("Y", "y"):
            sys.exit(1)
    try:
        # p = subprocess.Popen([RUN, NAME, 'runserver', SERVER_PORT])  # , stdout=subprocess.PIPE)
        # 生产环境 fork一个子进程保证线上安全
        p = subprocess.Popen('nohup {} {} runserver {}:{} &'.format(RUN, NAME, SERVER_HOSTS, SERVER_PORT), shell=True, preexec_fn=os.setsid)  # , stdout=subprocess.PIPE)
        # 生产环境
        # p = subprocess.Popen('nohup {} {} runserver {}:{} --noreload &'.format(RUN, NAME, SERVER_HOSTS, SERVER_PORT), shell=True, preexec_fn=os.setsid)#, stdout=subprocess.PIPE)
        p.wait()
        cmd = 'ps -ef | grep %s |grep -v "grep --color=auto" | ' \
              'grep %s | awk \'{print $2}\'' % (SERVER_PORT, cmd_server_name)
        ps_pid = os.popen(cmd).read().strip()
        print(ps_pid)
        monitor_pid = None
        pid = None
        if len(ps_pid.split("\n")) == 2:
            pid = ps_pid.split("\n")[0]
            monitor_pid = ps_pid.split("\n")[1]
        elif len(ps_pid.split("\n")) == 1:
            pid = ps_pid.split("\n")[0]
        else:
            sys.exit(1)
        if monitor_pid:
            print(" | ".join(["Start OK", "PID:%s" % pid]))
            print(" | ".join(["Start OK", "Monitor_PID:%s" % monitor_pid]))
            # daemonize(pidfile=SERVER_NAME_PIDFILE)
            open(PIDFILE, 'w+').write('{}\n{}'.format(pid,monitor_pid))
        else:
            print(" | ".join(["Start OK", "PID:%s" % pid]))
            # daemonize(pidfile=SERVER_NAME_PIDFILE)
            open(PIDFILE, 'w+').write('{}\n'.format(pid))
    except Exception as e:
        print(e)
    else:
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
        print(SERVER_NAME, " Stop error")
        return

    print("Stopping", SERVER_NAME, '...')
    if monitor_pid:
        if subprocess.call(["kill -9 " + monitor_pid], shell=True) == 0:
            time.sleep(0.2)
            pass
        else:
            print(SERVER_NAME, "monitor stop error")
    else:
        pass

    if pid:
        if subprocess.call(["kill -9  " + pid], shell=True) == 0:
            print(" | ".join(["Stop main process OK", "PID:%s" % pid]))
        if subprocess.call(["rm " + PIDFILE], shell=True) != 0:
            print("Delete Permission Denied")
        cmd = 'ps -ef | grep %s |grep -v "grep --color=auto" | ' \
              'grep %s | awk \'{print $2}\'' % (SERVER_PORT, cmd_server_name)
        ps_pid = os.popen(cmd).read().strip()
        if len(ps_pid.split("\n")) == 2:
            fork_pid = ps_pid.split("\n")[0]
            if subprocess.call(["kill -9  " + fork_pid], shell=True) == 0:
                print(" | ".join(["Stop fork process OK", "PID:%s" % fork_pid]))
        else:
            pass
    else:
        print("Stop Error")


def restart():
    stop()
    time.sleep(1)
    return start()


ops = {"start": start, "stop": stop, "restart": restart}

if __name__ == "__main__":
    pid = ops[OP]()
    # print(pid)
    # if OP == 'start' \
    #         or OP == 'restart':
    #
    #     cmd = 'ps -ef | grep %s | grep -v "grep" | ' \
    #           'grep %s | awk \'{print $2}\'' % (pid, cmd_server_name)
    #     ps_pid = os.popen(cmd).read().strip()
    #     print('ps_pid,pid', ps_pid, pid)
    #
    #     if ps_pid != pid:
    #         # pass
    #         subprocess.call(["rm " + PIDFILE], shell=True)
    #         pid = ops['start']()
    #     else:
    #         pass
    #     time.sleep(1)