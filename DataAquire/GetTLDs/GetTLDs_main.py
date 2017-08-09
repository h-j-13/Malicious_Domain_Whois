#!/usr/bin/python
# encoding:utf-8

#
# WhoisSrv获取-来自INNA
# func  : 主程序
# time  : old
# author: @`13
#

import time
from insert_info import GetTLD

Intervals = 3   # 获取内容时间间隔
GT = GetTLD()
while 1:
    GT.insertInfo(getIntervals=1)
    time.sleep(60*60*24)    # 获取间隔
