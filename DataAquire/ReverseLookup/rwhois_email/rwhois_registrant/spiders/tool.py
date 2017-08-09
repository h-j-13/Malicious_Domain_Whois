import MySQLdb as mdb


def get_cookie():
    con = mdb.connect('172.26.253.3', 'root', 'platform',
                      'cyn_malicious_domain', charset='utf8')
    cur = con.cursor()
    result = cur.execute("select * from benmi_cookie ")
    if (result != 0):
        cookie = cur.fetchall()[2]
    else:
        cookie = None
    con.close()
    return cookie


def delete_cookie(cookie):
    con = mdb.connect('172.26.253.3', 'root', 'platform',
                      'cyn_malicious_domain', charset='utf8')
    cur = con.cursor()
    result = cur.execute("delete from benmi_cookie where id = %s and  insert_time = %s", (cookie[0], cookie[3]))
    con.commit()
    con.close()
