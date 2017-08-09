#encoding:utf-8

from db_manage import MySQL
from datetime import datetime

def insert_svr():
    print str(datetime.now()),'开始更新二级服务器列表'
    db = MySQL()
    sql = 'INSERT INTO svr_ip(svr_name) SELECT DISTINCT sec_svr FROM top_sec_svr WHERE \
            NOT EXISTS  (SELECT svr_name FROM svr_ip WHERE svr_ip.svr_name=top_sec_svr.sec_svr)'
            
    db.insert(sql)
    db.close()
    print str(datetime.now()),'结束更新二级服务器列表'
    
    
#if __name__ == '__main__':
 #   print insert_svr()
