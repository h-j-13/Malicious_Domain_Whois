#!/usr/bin/env python
# encoding:utf-8
"""
    whois服务器通信
=====================

version   :   1.0
author    :   @`13
time      :   2017.1.18
"""

import socks

from Setting.static import Static
from WhoisConnect.server_ip import ServerIP

# Static().static_value_init()    # 静态值初始化
TIMEOUT = Static.SOCKS_TIMEOUT  # 超时设定
RECONNECT = Static.SOCKS_RECONNECT  # 最大重连数
Proxy_Flag = Static.PROXY_SOCKS_FLAG  # 使用代理标志
_proxy_socks = None

# 获取代理ip
if Proxy_Flag:
    from proxy_socks import ProxySocks

    _proxy_socks = ProxySocks()  # socks代理 获取对象
_server_ip = ServerIP()  # server_ip 获取对象


class WhoisConnectException(Exception):
    """whois 信息通信错误"""

    def __init__(self, value):
        self.value = value

    # @override
    def __str__(self):
        return str(self.value)


# 错误列表
error_list = ["ERROR -1",
              "ERROR -2",
              "ERROR -3",
              "ERROR OTHER"]

# 被ban列表/查询过快
ban_list = ["Queried interval is too short",
            "interval is too short",
            "The query frequency too fast"]


class GetWhoisInfo:
    """whois 通信类"""

    # 处理几个特殊的whois服务器（jp，de，com二级）
    def __init__(self, domain, whois_srv):
        """处理whois服务器"""
        # 处理特殊的请求格式
        if whois_srv == "whois.jprs.jp":
            self.request_data = "%s/e" % domain  # Suppress Japanese output
        elif domain.endswith(".de") and (whois_srv == "whois.denic.de" or whois_srv == "de.whois-servers.net"):
            self.request_data = "-T dn,ace %s" % domain  # regional specific stuff
        elif whois_srv == "whois.verisign-grs.com" or whois_srv == "whois.crsnic.net":
            self.request_data = "=%s" % domain  # Avoid partial matches
        else:
            self.request_data = domain
        self.whois_srv = whois_srv

    @staticmethod
    def _is_error(data):
        """判断返回数据中是否有错误"""
        return True if (data in error_list or data is None) else False

    def get(self):
        """获取数据"""
        data = ''
        for i in range(RECONNECT):  # 最大重连数
            data = self._connect()
            if not GetWhoisInfo._is_error(data):  # 如果数据没有错误,则直接返回
                break
        # 处理异常类型
        for ban_str in ban_list:  # 查询过快
            if data.find(ban_str) != -1:
                raise WhoisConnectException(5)
        if data in error_list:  # 如果在设定的错误类型中
            raise WhoisConnectException(error_list.index(data) + 1)
        elif data is None:  # 空数据
            raise WhoisConnectException(5)
        else:  # 正常情况
            return data

    def _connect(self):
        """核心函数：与whois通信
        需要：socks.py (ver 1.5.7)"""
        # whois服务器ip，代理ip
        global _server_ip, _proxy_socks
        host = _server_ip.get_server_ip(self.whois_srv)  # 服务器地址
        host = host if host else self.whois_srv  # 如果ip地址为空则使用服务器地址
        self.tcpCliSock = socks.socksocket()  # 创建socket对象
        self.tcpCliSock.settimeout(TIMEOUT)  # 设置超时时间
        if Proxy_Flag:  # socks代理配置
            proxy_info = _proxy_socks.get_proxy_socks(self.whois_srv)  # 代理IP
            if proxy_info is not None:
                # 设置代理
                if proxy_info['mode'] == 'SOCKS5':
                    self.tcpCliSock.set_proxy(proxy_type=socks.SOCKS5,  # socks类型
                                              addr=proxy_info['ip'],  # socks代地址
                                              port=proxy_info['port'],  # 端口
                                              username=proxy_info['username'],  # 用户名
                                              password=proxy_info['password'])  # 密码

                elif proxy_info['mode'] == 'SOCKS4':
                    self.tcpCliSock.set_proxy(proxy_type=socks.SOCKS4,  # socks类型
                                              addr=proxy_info['ip'],  # socks代地址
                                              port=proxy_info['port'])  # 端口
        data_result = ""
        try:
            self.tcpCliSock.connect((host, 43))  # 连接whois服务器
            self.tcpCliSock.send(self.request_data + '\r\n')  # 发出请求
        except Exception as e:  # Exception来自socks.py 中设置的异常
            if str(e).find("timed out") != -1 or \
                            str(e).find("TTL expired") != -1:  # 连接超时
                self.tcpCliSock.close()
                return "ERROR -1"
            elif str(e).find("Temporary failure in name resolution") != -1 or \
                            str(e).find("cannot connect to identd on the client") != -1 or \
                            str(e).find("unreachable") != -1:
                self.tcpCliSock.close()
                return "ERROR -2"
            else:
                self.tcpCliSock.close()
                return "ERROR OTHER"
        # 接收数据
        while True:
            try:
                data_rcv = self.tcpCliSock.recv(1024)  # 反复接收数据
            except:
                self.tcpCliSock.close()
                return "ERROR -3"
            if not len(data_rcv):
                self.tcpCliSock.close()
                return data_result  # 返回查询结果
            data_result = data_result + data_rcv  # 每次返回结果组合


def __Demo(Domain):
    domain = Domain  # 需要获取的域名
    whois_server = 'whois.afilias-grs.info.'  # 域名对应的whois服务器
    data_result = ''
    try:
        data_result = GetWhoisInfo(domain, whois_server).get()  # 获取
    except Exception as e:
        print e
    print "data->", data_result


if __name__ == '__main__':
    # Demo
    __Demo("yh888.bz")
