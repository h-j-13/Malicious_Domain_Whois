# !/usr/bin/python
# encoding:utf-8


# 与whois服务器通信, 获得其返回数据
# @author wangkai
# 2016.04.27

# last-update   ：2016.7.23
# change        ：修改了部分代码，使其可以读取配置文件
# @`13

import socket
from threading import Thread
import socks
from get_server_ip import ServerIP
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("WhoisClient.conf")
TIMEOUT = cf.getint('socket', 'timeout')
RECONNECT = cf.getint('socket', 'reconnect')

flag_proxy = cf.getint('proxy_ip', 'proxy_ip_flag')  # 使用代理标志
_proxy_ip = None

if flag_proxy:
    # from proxy_ip import ProxyIP
    _proxy_ip = None  # ProxyIP()  # 代理IP获取对象

_server_ip = ServerIP()  # server_ip 获取对象


# whois 信息通信错误
class WhoisConnectException(Exception):
    def __init__(self, value):
        self.value = value

    # @override
    def __str__(self):
        return str(self.value)


error_list = ['ERROR -1', 'ERROR -2', 'ERROR -3', 'ERRER OTHER', 'Queried interval is too short.']


def timelimited(timeout):
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


class GetWhoisInfo:
    def __init__(self, domain, whois_srv):
        if whois_srv == "whois.jprs.jp":
            self.request_data = "%s/e" % domain  # Suppress Japanese output
        elif domain.endswith(".de") and (whois_srv == "whois.denic.de" or whois_srv == "de.whois-servers.net" ):
            self.request_data = "-T dn,ace %s" % domain  # regional specific stuff
        elif whois_srv == "whois.verisign-grs.com" or whois_srv == "whois.crsnic.net":
            self.request_data = "=%s" % domain  # Avoid partial matches
        else:
            self.request_data = domain
        self.whois_srv = whois_srv

    @staticmethod
    def _is_error(data):
        return True if (data in error_list or data is not None) else False

    def get(self):
        data = ''
        for i in range(RECONNECT):
            self.tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data = self._connect()
            self.tcpCliSock.close()
            if not GetWhoisInfo._is_error(data):
                break

        if data in error_list:
            raise WhoisConnectException(error_list.index(data) + 1)
        elif data is None:
            raise WhoisConnectException(4)
        else:
            return data

    @timelimited(TIMEOUT)
    def _connect(self):
        global _server_ip, _proxy_ip
        host = _server_ip.get_server_ip(self.whois_srv)  # 服务器地址
        host = host if host else self.whois_srv
        if flag_proxy:
            proxy_info = _proxy_ip.get(self.whois_srv)  # 代理IP
            if proxy_info is not None:
                socks.setdefaultproxy(
                        proxytype=socks.PROXY_TYPE_SOCKS4 if proxy_info.mode == 4 else socks.PROXY_TYPE_SOCKS5,
                        addr=proxy_info.ip,
                        port=proxy_info.port)
                socket.socket = socks.socksocket
                self.tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(20)
        data_result = ""
        try:
            self.tcpCliSock.connect((host, 43))
            self.tcpCliSock.send(self.request_data + '\r\n')
        except socket.error as e:
            if str(e).find("timed out") != -1:  # 连接超时
                return "ERROR -1"
            elif str(e).find("Temporary failure in name resolution") != -1:
                return "ERROR -2"
            else:
                return "ERROR OTHER"

        while True:
            try:
                data_rcv = self.tcpCliSock.recv(1024)
            except socket.error as e:
                return "ERROR -3"
            if not len(data_rcv):
                return data_result  # 返回查询结果
            data_result = data_result + data_rcv  # 每次返回结果组合


class TimeoutException(Exception):
    pass


def test():
    domain = 'nintendo.co.jp'  # raw_input("domain :")
    whois_server = 'whois.jprs.jp'  # raw_input("whois_server :")
    import time
    begin_time = time.time()
    try:
        data_result = GetWhoisInfo(domain, whois_server).get()
    except Exception:
        pass
    print time.time() - begin_time
    print data_result


if __name__ == '__main__':
    test()
