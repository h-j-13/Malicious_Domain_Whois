#!/usr/bin/env python
# encoding:utf-8

import os
import MySQLdb as mdb
from time import sleep


def get_registrant_num():
    """获取需要反查的记录数"""
    try:
        con = mdb.connect('172.26.253.3',
                          'root',
                          'platform',
                          'malicious_domain_sys',
                          charset='utf8')
        cur = con.cursor()
        record_num = cur.execute(
            """SELECT * FROM malicious_domain_sys.info_reverse_search WHERE done != 1 AND info_type = 4 LIMIT 1 """)
        con.close()
    except Exception as Error:
        print Error
        return 0
    return record_num


def main():
    """启动Scrapy 主程序循环"""
    num = get_registrant_num()
    while num:
        os.system("scrapy crawl rwhois_phone")
        sleep(5)
        num = get_registrant_num()


if __name__ == '__main__':
    main()
