# /usr/bin/python
# encoding:utf8


# 静态资源及路径设置
# @author wangkai
# @version 1.0
# 2015.12.23


import ConfigParser
import logging
import logging.config
import datetime
import os
import sys

# reload(sys)

class Static:
    PROCESS_MAX = None  # 处理线程上限
    RABBITMQ_HOST = None  # rabbitmq服务器地址
    LIMIT_COUNT = None  #
    WEB_SERVER_PORT = None  # API服务端口
    COMMIT_NUM = None  # 事务提交数
    FINISHED_TLD = None  # 完成tld
    PATH_SERVER_FUNCTION = None  # server_func 文件路径
    PATH_LOGGER_CONF = None  # 日志系统配置文件
    PATH_CONF = None  # 配置文件路径

    logger = None  # 日志记录对象
    logger_db = None  # 数据库日志记录对象
    whois_db = None  # 主数据库操作对象
    whois_addr_db = None  # whois address 数据库操作对象
    func_name = None  # 域名处理函数获取对象
    whois_addr = None  # whois服务器获取对象

    # 静态对象初始化
    @staticmethod
    def init():
        Static.static_value_init()
        Static.object_init()
        Static.whois_server_info_init()

    # 静态值初始化
    @staticmethod
    def static_value_init():
        sys.path.append('..')
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
        sys.path.append(root_path)

        Static.PATH_CONF = root_path + 'domain_whois.conf'
        Static.PATH_LOGGER_CONF = root_path + 'logger.conf'
        Static.PATH_SERVER_FUNCTION = root_path + 'data/.server_function'
        try:
            conf = ConfigParser.ConfigParser()
            conf.read(Static.PATH_CONF)
            Static.PROCESS_MAX = int(conf.get('线程上限', 'PROCESS_MAX'))
            Static.RABBITMQ_HOST = conf.get('rabbitmq服务器地址', 'RABBITMQ_HOST')
            Static.LIMIT_COUNT = conf.get('读取限制数', 'LIMIT_COUNT')
            Static.WEB_SERVER_PORT = conf.get('WEB服务端口', 'WEB_SERVER_PORT')
            Static.COMMIT_NUM = conf.get('commit次数', 'COMMIT_NUM')
        except Exception as e:
            print '配置文件读取出错: ' + str(e)
            exit(0)

    # 对象出初始化
    @staticmethod
    def object_init():
        logging.config.fileConfig(Static.PATH_LOGGER_CONF)
        Static.logger = logging.getLogger("whois_info_deal")
        Static.logger_db = logging.getLogger("db_operation")
        from data import WhoisAddrDataBase, WhoisDataBase
        Static.whois_db = WhoisDataBase()  # Whois数据库操作对象, 进行whois数据查询更新的对象
        Static.whois_addr_db = WhoisAddrDataBase()  # whois_addr 数据库操作对象

    # 初始化域名信息相关
    @staticmethod
    def whois_server_info_init():
        Static.whois_addr_db.connect()
        from data import WhoisServerAddr, FuncName
        Static.whois_addr = WhoisServerAddr(Static.whois_addr_db)
        Static.func_name = FuncName(Static.whois_addr_db, Static.PATH_SERVER_FUNCTION)
        Static.FINISHED_TLD = Static.func_name.get_finished_tld()
        try:
            Static.FINISHED_TLD.remove('com')
            Static.FINISHED_TLD.remove('net')
        except KeyError:
            pass
        Static.whois_addr_db.close()

    @staticmethod
    def get_now_time():
        return str(datetime.datetime.now()).split('.')[0]

if __name__ == '__main__':
    Static.init()
    print Static.PATH_CONF
    print Static.get_now_time()






