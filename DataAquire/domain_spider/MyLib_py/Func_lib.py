#!/usr/bin/python
# encoding:utf-8

"""
    其他常用函数的库

author     :   @`13
version    :   0.1.0
last-update:   2016.8.13

# history：
version 0.1.0
    *   + 超时装饰器
    *   + 时间处理
"""

import time
import datetime
from threading import Thread

# 函数处理事件上限装饰器
def timelimited(timeout):
    """
    :param timeout:时间上限（int/float）
    当装饰器装饰的函数的运行时间达到设定的时间上限时，
    装饰器回将其强行中断,并Rasie一个可以重写的超时错误
    """
    def decorator(function):
        def decorator2(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self, _error=None, ):
                    Thread.__init__(self)
                    self._error = _error
                    self.result = None
                def run(self):
                    try:
                        self.result = function(*args, **kwargs)
                    except Exception, e:
                        self._error = e
                def _stop(self):
                    if self.isAlive():
                        ThreadStop = Thread._Thread__stop
                        ThreadStop(self)
            t = TimeLimited()
            t.setDaemon(True)  # 守护线程
            t.start()
            t.join(timeout)
            if isinstance(t._error, TimeoutException):
                t._stop()
                return 'ERROR -1'  # 超时
            if t.isAlive():
                t._stop()
                return 'ERROR -1'  # 超时
            if t._error is None:
                t._stop()
                return t.result
        return decorator2
    return decorator


class TimeoutException(Exception):
    # 超时异常
    #
    # A demo [可供重写
    # --------------------------
    # def __init__(self, value):
    #     self.value = value
    #     self.error_list = ['error type：error detail', '...']
    #
    # # @override
    # def __str__(self):
    #     return str(self.error_list[self.value])
    pass

# 调用Demo
# @timelimited(0)
# def sleep():
#     time.sleep(100)


def getLocalTime(Timeformat=None, returnType='str'):
    """
    获取本地时间
    :param Timeformat: 需要传入一个时间格式 [默认使用ISO标准]
    :param returnType: 返回数据的类型      [默认为str] 支持datetime/...
    :return: 当前时间(字符串格式）
    """
    __ISOTIMEFORMAT = '%Y-%m-%d %X'     # ISO时间标准
    if not Timeformat:
        Timeformat = __ISOTIMEFORMAT
    __now_time_str = time.strftime(Timeformat, time.gmtime(time.time()))

    if returnType.find('datetime') != -1:
        return datetime.datetime.strptime(__now_time_str, Timeformat)
    else:
        return __now_time_str

if __name__ == '__main__':
    getLocalTime()
