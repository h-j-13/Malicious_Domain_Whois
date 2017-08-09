import MySQLdb
import random

s="SELECT ID FROM domain_index where judge_flag=-1 and judge_score=-100 limit 1000"
ss="UPDATE domain_index SET judge_score=%s where ID=%s"

con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
cur=con.cursor()

cur.execute(s)
result=cur.fetchall()
for item in result:
    print item,random.random()*100
    cur.execute(ss%(random.random()*100,item[0]))
    con.commit()
