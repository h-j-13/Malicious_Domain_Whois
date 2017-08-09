#!/usr/bin/env python
# encoding:utf-8

"""
    获取域名whois数据
=======================

version   :   1.0
author    :   @`13
time      :   2017.1.18
"""

from Setting.global_resource import *  # 全局资源
from Setting.static import Static  # 静态变量,设置
from WhoisConnect import whois_connect  # Whois通信
from WhoisData.info_deal import get_result  # Whois处理函数
from Database.update_record import WhoisRecord  # 更新信息函数
from Database.db_opreation import DataBase  # 数据库对象

Static.init()
Resource.global_object_init()
log_get_whois = Static.LOGGER


def get_domain_whois(raw_domain=""):
    """
    获取whois信息
    :param raw_domain: 输入域名
    :return: whois信息字典 / 获取失败返回None
    """
    log_get_whois.info(raw_domain + ' - start')

    # 处理域名信息
    Domain = Resource.Domain(raw_domain)
    # domain = Domain.get_utf8_domain()  # 用于返回显示的域名（utf8格式）
    domain_punycode = Domain.get_punycode_domain()  # punycode编码域名
    tld = Domain.get_tld()  # 域名后缀
    WhoisSerAddr = Resource.TLD.get_server_addr(tld)  # 获取whois地址,失败=None
    WhoisSerIP = Resource.WhoisSrv.get_server_ip(WhoisSerAddr)  # 获取whois地址的ip(随机取一个),失败=None
    WhoisFunc = Resource.WhoisFunc.get_whois_func(WhoisSerAddr)  # 获取TLD对应的提取函数名称

    log_get_whois.info('whois : ' +
                       str(WhoisSerAddr) +
                       '->' + str(WhoisSerIP) +
                       ' use:' + str(WhoisFunc))

    # 获取用于通信的whois服务器地址
    # 优先级 : ip > whois地址 > None (失败)
    WhoisConnectAddr = WhoisSerIP
    if WhoisConnectAddr is None:
        WhoisConnectAddr = WhoisSerAddr
    if not WhoisConnectAddr:
        log_get_whois.error(raw_domain + ' - fail : whois通信地址获取失败')
        return None

    # 获取原始whois数据
    raw_whois_data = ''  # 原始whois数据
    data_flag = 1  # whois通信标记
    try:
        raw_whois_data = whois_connect.GetWhoisInfo(domain_punycode, WhoisConnectAddr).get()
    except whois_connect.WhoisConnectException as connect_error:
        data_flag = 0 - int(str(connect_error))
    if raw_whois_data is None:
        data_flag = -5  # 获取到空数据，flag = -5

    # 处理原始whois数据
    log_get_whois.info('flag : ' + str(data_flag))

    whois_dict = get_result(domain_punycode,
                            tld,
                            str(WhoisSerAddr),
                            WhoisFunc,
                            raw_whois_data,
                            data_flag)

    log_get_whois.info(raw_domain + ' - finish')
    return whois_dict

def GetDomainWhois(domain):
    whois_dict = get_domain_whois(domain)
    DB = DataBase()
    DB.db_connect()
    WhoisRecord(DB).Update(whois_dict, -99)
    DB.db_commit()
    DB.db_close()


if __name__ == '__main__':
    # Demo
    GetDomainWhois('fjteaw.cn')
