#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : Joshua
@Time    : 2019/3/5 18:28
@File    : nlp_server.py
@Desc    : 
"""

from src.utils.daemonize import *
import getopt
import sys


if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:], '-h', ['help'])
    if args[2]:
        daemonize('./.nlp_server_pidfile')
    else:
        PORT = 1

    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[*] Help info")
            exit()



