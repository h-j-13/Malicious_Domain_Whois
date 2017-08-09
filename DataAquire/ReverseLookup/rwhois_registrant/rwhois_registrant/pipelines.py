#!/usr/bin/env python
# encoding:utf-8

import MySQLdb as mdb
import time


class RwhoisRegistrantPipeline(object):
    """pipeline"""

    def __init__(self):
        """连接到数据库"""
        try:
            self.con = mdb.connect('172.26.253.3',
                                   'root',
                                   'platform',
                                   'malicious_domain_sys',
                                   charset='utf8')
        except Exception as MySQLError:
            msg = str(MySQLError)
            print msg
            self.output_msg(msg)

    def process_item(self, item, spider):
        """插入数据库"""
        try:
            print item.items
            cur = self.con.cursor()
            insert_date = self.get_time()

            cur.execute(
                """INSERT INTO malicious_domain_sys.domain_index(ID, domain, source) values(%s,%s,%s) """,
                (hash(item["domain"].rstrip()), item["domain"].rstrip(), '12'))
            self.con.commit()
            return item
        except Exception, e:
            f = open("data.log", 'a')
            msg = item["domain"] + ";" + item["registrant"] + ";" + str(insert_date) + str(e) + '\n'
            f.write(msg)
            f.close()

    def close_spider(self, spider):
        self.con.close()

    def output_msg(self, msg):
        FORM = '%Y/%m/%d  %H:%M:%S'
        data = time.localtime(time.time())
        output_time = time.strftime(FORM, data)
        output_file = open('./result.log', 'a')
        message = output_time + '   ' + msg + '\n'
        output_file.write(message)
        output_file.close()
        return message

    def get_time(self):
        FORM = '%Y/%m/%d  %H:%M:%S'
        data = time.localtime(time.time())
        output_time = time.strftime(FORM, data)
        return output_time
