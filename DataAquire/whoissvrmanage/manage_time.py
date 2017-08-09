#!/usr/bin/python
#encoding:utf-8

import sys
import time
from reverse import get_svr_ip
from verify_port import verify_ip_whois
from insert_svr import insert_svr

sys.stdout.flush()
try:
    import schedule
except ImportError:
    sys.exit("无schedul模块,请安装 easy_install schedule")


if __name__ == "__main__":
    
    schedule.every(0).minutes.do(get_svr_ip)   # 获取域名ip以及验证
    schedule.every(0).minutes.do(verify_ip_whois)  # 验证
    #schedule.every(30).minutes.do(insert_svr)  # 更新二级whois服务器列表
    while True:
        schedule.run_pending()
        time.sleep(1)
