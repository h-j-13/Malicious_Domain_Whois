import MySQLdb

# s="select ID from domain_index where ID not in (select ID from other_info) and judge_flag!=-10"
#
# ss="select d.ID,judge_flag from domain_index d,other_info o where o.ID = d.ID and o.web_judge_result=-100 and d.judge_flag!=-10"
#
# sss="UPDATE domain_index d, other_info o SET o.web_judge_result=d.judge_flag WHERE o.ID=d.ID and d.ID=-9223303839817319818"
#
# ssss="SELECT ID,other_info_flag,judge_flag from domain_index where ID in (select ID from other_info where web_judge_result!=-100 and web_judge_result!=-10 and web_judge_result!=-1 and web_judge_result!=4)"
#
# sssss="UPDATE domain_index SET other_info_flag = %s where ID = %s"

s="SELECT ID,Alex,web_judge_result from other_info "

con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
cur=con.cursor()
cur.execute(s)

def to_full_flag(flag):
    i=int(flag)
    return flag/100*100+flag%10+10


# r=cur.fetchmany(500)
r=cur.fetchall()

while True:
    for item in r:
        if item[1]=='--':
            if item[2] in [1,2,3]:
                cur.execute("UPDATE domain_index SET other_info_flag=1 where ID=%s"%item[0])
                print item[0],item[1],item[2],110
            else:
                cur.execute("UPDATE domain_index SET other_info_flag=2 where ID=%s"%item[0])
                print item[0],item[1],item[2],100
        elif item[1]=='':
            if item[2] in [1,2,3]:
                cur.execute("UPDATE domain_index SET other_info_flag=3 where ID=%s"%item[0])
                print item[0],item[1],item[2],310
            else:
                cur.execute("UPDATE domain_index SET other_info_flag=4 where ID=%s"%item[0])
                print item[0],item[1],item[2],300

        else:
            if item[2] in [1,2,3]:
                cur.execute("UPDATE domain_index SET other_info_flag=5 where ID=%s"%item[0])
                # print item[0],item[1],item[2]
                print item[0],item[1],item[2],210
            else:
                cur.execute("UPDATE domain_index SET other_info_flag=6 where ID=%s"%item[0])
                print item[0],item[1],item[2],200
    con.commit()
    break
        # print item[0],item[1],item[2],to_full_flag(item[1])
        # sql=sssss%(to_full_flag(item[1]),item[0])
        # cur.execute(sql)
    # con.commit()
    # r=cur.fetchmany(500)
    if len(r)==0:
        break
print len(r)
con.commit()
