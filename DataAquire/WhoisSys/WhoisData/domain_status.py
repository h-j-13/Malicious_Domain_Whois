#!/usr/bin/env python
# encoding:utf-8

"""
    确定域名状态值,将域名状态转换成状态值
==================================

version   :   1.0
author    :   @`13
time      :   2017.2.8
"""

# 状态值字典
status_dict = {
    # EPP
    'ADDPERIOD': '1',
    'AUTORENEWPERIOD': '2',
    'INACTIVE': '3',
    'OK': '4',
    'PENDINGCREATE': '5',
    'PENDINGDELETE': '6',
    'PENDINGRENEW': '7',
    'PENDINGRESTORE': '8',
    'PENDINGTRANSFER': '9',
    'PENDINGUPDATE': '10',
    'REDEMPTIONPERIOD': '11',
    'RENEWPERIOD': '12',
    'SERVERDELETEPROHIBITED': '13',
    'SERVERHOLD': '14',
    'SERVERRENEWPROHIBITED': '15',
    'SERVERTRANSFERPROHIBITED': '16',
    'SERVERUPDATEPROHIBITED': '17',
    'TRANSFERPERIOD': '18',
    'CLIENTDELETEPROHIBITED': '19',
    'CLIENTHOLD': '20',
    'CLIENTRENEWPROHIBITED': '21',
    'CLIENTTRANSFERPROHIBITED': '22',
    'CLIENTUPDATEPROHIBITED': '23',
    # RRP
    'ACTIVE': '24',
    'REGISTRYLOCK': '25',
    'REGISTRARLOCK': '26',
    'REGISTRYHOLD': '27',
    'REGISTRARHOLD': '28',
    # 'REDEMPTIONPERIOD': '29', 重复
    # 'PENDINGRESTORE': '30', 重复
    # 'PENDINGDELETE': '31', 重复
    'NOTEXIST': '29',  # 域名不存在
    'NOSTATUS': '30',  # 无状态值
    'CONNECT': '31',  # de服务器状态
}

def get_status_value(status_str):
    """
    将域名状态字符串转换成状态值
    :param status_str: 域名状态字符串
    :param domain:
    :return: 状态值［若无状态则默认为30(NOSTATUS),
                   非标准状态值只变成大写"""
    status_return = ''
    if status_str == '':
        return '30'
    infos = status_unite(status_str).split(';')
    for status in infos:
        status_value = status_dict.get(status, '0')
        if status_value == '0':
            status_value = status
        status_return += status_value
        status_return += ';'
    return status_return.strip(';')


def status_unite(status):
    """状态字符串格式处理"""
    while status.find(' ') != -1:
        status = status.replace(' ', ';')
    while status.find('-') != -1:
        status = status.replace('-', ';')
    return status.upper()


if __name__ == '__main__':
    # Demo
    print get_status_value('other ADDPERIOD-INACTIVE')
