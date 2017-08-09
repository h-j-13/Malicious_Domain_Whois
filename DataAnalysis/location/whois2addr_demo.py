#coding=utf-8
import sys
from whois2addr import Whois2Addr

reload(sys)
sys.setdefaultencoding('utf-8')

w2a = Whois2Addr()
result = w2a.analyze('shandong', 'weihai')
print result[0], result[1]
result = w2a.analyze('ShandongSheng', 'WeihaiShi')
print result[0], result[1]

