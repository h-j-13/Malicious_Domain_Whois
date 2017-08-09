#!/usr/bin/python
# encoding:utf-8

"""
    简单封装的日志记录类

author     :   @`13
version    :   0.0.1
last-update:   2016.9.28

# history：
version 0.0.1
    *   + 简单封装 （非正式版
            没有使用logging，只是对现在的需求写了一个简单地封装类
            调用是要初始化这个类的对象
"""

# import logging
import time
import datetime
import threading


class MyLog:
    def __init__(self, filename, path=None):
        """
        :param filename: 日志文件名,
        """
        self.logLock = threading.Lock()
        if path:
            __filePathName = path + filename
        else:
            __filePathName = filename+'.log'
        self.logfile = open(__filePathName, "w")
        self.logMassage('初始化日志文件', infoLevel='log')

    @staticmethod
    def getLocalTime(Timeformat=None, returnType='str'):
        """
        获取本地时间
        :param Timeformat: 需要传入一个时间格式 [默认使用ISO标准]
        :param returnType: 返回数据的类型      [默认为str] 支持datetime/...
        :return: 当前时间(字符串格式）
        """
        __ISOTIMEFORMAT = '%Y-%m-%d %X'  # ISO时间标准
        if not Timeformat:
            Timeformat = __ISOTIMEFORMAT
        __now_time_str = time.strftime(Timeformat, time.gmtime(time.time()))

        if returnType.find('datetime') != -1:
            return datetime.datetime.strptime(__now_time_str, Timeformat)
        else:
            return __now_time_str

    def logMassage(self, info, infoLevel='Debug', isPrint=False):
        """
        记录内容类
        :param info: 需要记录的信息
        :param infoLevel: 信息等级
        :param isPrint: 是否需要打印到屏幕中
        """
        if self.logLock.acquire():  # 保证写入操作是线程安全的
            __time = self.getLocalTime()
            __massage = __time    # 时间
            __massage += '\t['+infoLevel+']\t'  # 日志等级
            __massage += info
            self.logfile.write(__massage + '\n')
            if isPrint:
                print __massage
            self.logLock.release()

    def close(self):
        """关闭日志文件对象"""
        self.logMassage('日志文件关闭', infoLevel='log')
        self.logfile.close()


if __name__ == '__main__':
    L = MyLog('test')
    L.logMassage('test',isPrint=True)
    L.close()
