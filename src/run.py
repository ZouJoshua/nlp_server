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
    print("ServerName:\n>> news_category\n>> news_regional\n>> news_parser\n>> news_taste\n>> video_category\n>> video_tags")
    sys.exit("Usage:sudo %s {ServerName} {start, stop, restart}" % SCRPET)

RUN = "python3"
SERVER_NAME = sys.argv[1]
NAME = sys.argv[2]
OP = sys.argv[3]

# 服务环境设置
def set_environ(server_name,server_host):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.environ.setdefault("NLP_SERVER_NAME", server_name)
    os.environ.setdefault("SERVER_HOSTS", server_host)
    config_file = "{}_conf".format(server_name)
    if os.path.exists(os.path.join(BASE_DIR, 'config', config_file+'.py')):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.{}".format(config_file))
    else:
        raise Exception("{}服务配置文件不存在，请检查".format(server_name))
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.base_conf")
    server_hosts = os.environ.get('SERVER_HOSTS', '127.0.0.1')
    if server_name =='news_category':
        # server ip
        server_port = os.environ.get('PORT', 19901)
    elif server_name == 'news_regional':
        server_port = os.environ.get('PORT', 18801)
    elif server_name == 'news_parser':
        server_port = os.environ.get('PORT', 8020)
    elif server_name == 'news_taste':
        server_port = os.environ.get('PORT', 16601)
    elif server_name == 'video_category':
        server_port = os.environ.get('PORT', 17701)
    elif server_name == 'video_tags':
        server_port = os.environ.get('PORT', 9022)
    else:
        server_port = os.environ.get('PORT', 10901)
    return server_hosts, server_port

server_host= "127.0.0.1"
SERVER_HOSTS, SERVER_PORT = set_environ(SERVER_NAME, server_host)
# 服务pid监控
SERVER_NAME_PIDFILE = '.{}_pidfile'.format(SERVER_NAME)
PIDFILE = "{}/{}".format(HOME, SERVER_NAME_PIDFILE)
cmd_server_name = os.path.split(os.path.realpath(NAME))[-1].replace('.py', '')

# 启动
def start():
    # print(" | ".join([HOME, NAME]))
    print("Starting {} server on\nhttp://{}:{}...".format(SERVER_NAME, SERVER_HOSTS, SERVER_PORT))
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
        time.sleep(1)
        ppid = None
        pid = None
        cmd = 'ps -ef | grep %s |grep -v "grep --color=auto" | ' \
              'grep %s | awk \'{print $2}\'' % (SERVER_PORT, cmd_server_name)
        ps_pid = os.popen(cmd).read().strip()
        if len(ps_pid.split("\n")) == 2:
            ppid = ps_pid.split("\n")[0]
            pid = ps_pid.split("\n")[1]
        elif len(ps_pid.split("\n")) == 1:
            pid = ps_pid.split("\n")[0]
        else:
            raise Exception('PID Process error, please check')
            # sys.exit(1)
        if ppid and pid:
            print(" | ".join(["Start OK", "PID:%s" % pid]))
            print(" | ".join(["Start OK", "PPID:%s" % ppid]))
            # daemonize(pidfile=SERVER_NAME_PIDFILE)
            open(PIDFILE, 'w+').write('{}\n{}\n'.format(pid, ppid))
        elif pid:
            print(" | ".join(["Start OK", "PID:%s" % pid]))
            # daemonize(pidfile=SERVER_NAME_PIDFILE)
            open(PIDFILE, 'w+').write('{}\n'.format(pid))
        else:
            raise Exception('Start error...')
    except Exception as e:
        print(e)
    else:
        return pid

# 停止
def stop():
    if not os.path.exists(PIDFILE):
        return
    pid_list = open(PIDFILE).readlines()
    pid = None
    ppid = None
    if len(pid_list) == 1:
        pid = pid_list[0].strip()
    elif len(pid_list) == 2:
        pid = pid_list[0].strip()
        ppid = pid_list[1].strip()
    else:
        print(SERVER_NAME, " Stop error...")
        return

    print("Stopping", SERVER_NAME, '...')
    if ppid and pid:
        if subprocess.call(["kill -9 " + pid], shell=True) == 0:
            print(" | ".join(["Stop main process OK", "PID:%s" % pid]))
        if subprocess.call(["kill -9 " + ppid], shell=True) == 0:
            print(" | ".join(["Stop parent process OK", "PID:%s" % ppid]))
        if subprocess.call(["rm " + PIDFILE], shell=True) != 0:
            print("Delete Permission Denied")
        else:
            print(SERVER_NAME, "pid file delete...")
    elif pid:
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
                print(" | ".join(["Stop parent process OK", "PID:%s" % fork_pid]))
        else:
            pass
    else:
        print("Stop Error..")

# 重启
def restart():
    stop()
    time.sleep(1)
    return start()


ops = {"start": start, "stop": stop, "restart": restart}

if __name__ == "__main__":
    pid = ops[OP]()
