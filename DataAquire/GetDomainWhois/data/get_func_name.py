# /usr/bin/python
# encoding:utf8

# 获取whois服务器对应的函数名称
# @version 1.0
# @author wangkai
# 2015.12.5

from domain_analyse import DomainAnalyse


class FuncName:
    def __init__(self, db, path_server_function):
        self.finished_tld_list = []  # 完成后缀表
        file_server_function = open(path_server_function)
        self.server_function_dict = {}
        for line in file_server_function.readlines():
            info_list = line.split(':')
            whois_server = info_list[0].strip()
            func_name = info_list[1].strip()
            self.server_function_dict.setdefault(whois_server, func_name)
            if whois_server is None or whois_server == '':
                continue
            for result in db.get_tld(whois_server):
                self.finished_tld_list.append(DomainAnalyse.get_punycode(result.tld))
        file_server_function.close()

    def get_finished_tld(self):
        while None in self.finished_tld_list:
            self.finished_tld_list.remove(None)
        return set(self.finished_tld_list)

    # 获取处理函数名称
    def get_func_name(self, server_addr):
        return self.server_function_dict.get(server_addr, None)


