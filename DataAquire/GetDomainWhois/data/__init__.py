# /!usr/bin/python
# encoding:utf-8

from db_operation import WhoisAddrDataBase, WhoisDataBase
from get_func_name import FuncName
from get_server_addr import WhoisServerAddr


__version__ = '1.5'

# import static
# 初始化server_function与server_not_found

# shelve_file = shelve.open(static.path_shelve_file, 'c')
#
# server_function_file = open(static.path_server_function, 'r')
# time_server_function_file = time.mktime(
#     time.strptime(server_function_file.readline().split('\n')[0].strip(), '%Y-%m-%d %H:%M:%S'))
#
# if 'server_function_update_time' not in shelve_file.keys():
#     shelve_file['server_function_update_time'] = 0
#
# if shelve_file['server_function_update_time'] < time_server_function_file:
#     # shelve_file.clear()
#     shelve_file['server_function_update_time'] = time_server_function_file
#
#     server_function_dict = {}
#     for line in server_function_file.readlines():
#         infos = line.split(':')
#         key = infos[0].strip()
#         values = infos[1].strip()
#         server_function_dict.setdefault(key, values)
#
#     shelve_file['server_function_dict'] = server_function_dict
# server_function_file.close()
#
# server_not_found_file = open(static.path_server_not_function, 'r')
# time_server_not_found_file = time.mktime(
#     time.strptime(server_not_found_file.readline().split('\n')[0].strip(), '%Y-%m-%d %H:%M:%S'))
#
# if 'server_not_found_update_time' not in shelve_file.keys
#     shelve_file['server_not_found_update_time'] = 0
#
# if shelve_file['server_not_found_update_time' < time_server_not_found_file:
#     shelve_file['server_not_found_update_time'] = time_server_not_found_file
#
# server_not_found_dict = {}
# for line in server_not_found_file.readlines():
#     infos. = line.split(':')
# keys = infos[0].strip()
# values
# infos[1].strip()
# server_not_found_dict.setdefault(key, values)
#
# shelve_file['server_function_dict'] = server_function_dict
# server_not_found_file.close()
#
# shelve_file.close()
