# /usr/bin/python
# encoding:utf8


# 静态资源及路径设置
# @author wangkai
# @version 1.0
# 2015.12.23


import ConfigParser
import logging
import logging.config
import os
import sys


# 获取一个新的数据库操作对象
def newDB():
    return data_get.db_operation.DataBase()


now_path = os.path.abspath('./')

if now_path.find('GetDomainWhois/') == -1:
    root_path = now_path + '/'
else:
    root_path = '/'
    now_path_list = (now_path + '/').split('/')
    length_now_path = len(now_path_list) - 2
    for i, path in enumerate(now_path_list):
        if i != length_now_path and path:
            root_path += path
            root_path += '/'

path_domain_whois_conf = root_path + 'domain_whois.conf'
path_logger_conf = root_path + 'logger.conf'
path_server_function = root_path + 'data_get/.server_function'
path_server_function_shelve = root_path + 'data_get/server_function'

sys.path.append(root_path)

logging.config.fileConfig(path_logger_conf)
logger = logging.getLogger("example_3")
logger_db = logging.getLogger("example_db")

conf = ConfigParser.ConfigParser()
try:
    conf.read(path_domain_whois_conf)
    TABLE_WHOIS_ADDR = conf.get('whois服务器地址表', 'TABLE_WHOIS_ADDR')
    DB_HOST = conf.get("数据库地址", 'DB_HOST')
    USERNAME = conf.get('用户名', 'USERNAME')
    PASSWORD = conf.get('密码', 'PASSWORD')
    READ_NUM = conf.get('读取数量', 'READ_NUM')
    TABLE_PROXY = conf.get('代理IP表', 'TABLE_PROXY')
    PROCESS_MAX = int(conf.get('线程上限', 'PROCESS_MAX'))
    TEST_COUNT = int(conf.get('测试次数', 'TEST_COUNT'))
    INIT_TABLES = conf.get('初始数据建立读取表', 'INIT_TABLES').split(',')
    TABLE_SPV_IP = conf.get('whois服务器ip地址表', 'TABLE_SRV_IP')
except Exception, e:
    logger.error('配置文件读取出错 error_info: ', e)

import data_get

main_DB = data_get.db_operation.DataBase()  # 数据库操作对象， 进行whois数据查询更新的主要对象
server_addr = data_get.get_server_addr.ServerAddr()  # server_addr服务器地址 获取对象
func_name = data_get.get_func_name.FuncName()  # func_name 获取对象
server_ip = data_get.get_server_ip.ServerIP()  # server_ip 获取对象
