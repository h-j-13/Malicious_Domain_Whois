# -*- coding: utf-8 -*-

# coding: utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# coding: utf-8

import MySQLdb as mdb
import time


class RwhoisRegistrantPipeline(object):
    def __init__(self):
        try:
            self.con = mdb.connect('172.26.253.3',
                                   'root',
                                   'platform',
                                   'malicious_domain_sys',
                                   charset='utf8')
        except Exception as e:
            msg = 'datebase error:' + str(e)
            print msg
            self.output_msg(msg)

    def process_item(self, item, spider):
        try:
            print item.items
            cur = self.con.cursor()
            insert_date = self.get_time()
            cur.execute(
                """INSERT INTO malicious_domain_sys.domain_index(ID, domain, source) values(%s,%s,%s) """,
                (hash(item["domain"].rstrip()), item["domain"].rstrip(), '13'))
            self.con.commit()
            return item
        except Exception, e:
            print '!!!!!!!!!!' + str(e)
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
