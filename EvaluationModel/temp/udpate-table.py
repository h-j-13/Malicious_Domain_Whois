import MySQLdb

con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
cur=con.cursor()


# s="SELECT d.ID,substring(w.flag,-1) from domain_index d,malicious_info m WHERE d.ID=m.ID and judge_flag=-1 limit 1000"
# s="SELECT ID,substring(flag,-1) from malicious_info where flag!=0 limit 500"
s="select ID from (select ID,substring(flag,-1) as f from malicious_info )t where t.f=2;"

cur.execute(s)
while True:
    result=cur.fetchmany(500)
    if len(result)==0:
        break
    for item in result:
        cur.execute("update domain_index set judge_flag=-3 where id=%s"%item[0])
        con.commit()
    # for item in result:
        # if item[1]==1 or item[1]==2:
            # print item[0],item[1]
