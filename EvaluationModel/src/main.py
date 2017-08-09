#!coding:utf-8

import config
import BaseSQL
import ConfigUpdater
import MalProbability
import DecisionTree
import ThreadEntry
import Utilities
import MySQLdb
import Queue
import csv
import sys
from time import sleep

domains=Queue.Queue()
samples=Queue.Queue()
predicts=Queue.Queue()

def get_domains():
    """
        for model-build,只选择信息完整的域名
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    s="select domain,judge_flag from domain_index where ID in %s"%BaseSQL.full_data_id
    cur.execute(s)
    while True:
        if domains.empty():
            r=cur.fetchmany(100)
            if len(r)==0:
                return
            for d in r:
                domains.put([d[0],d[1]])
        else:
            sleep(1)

def get_domain_to_predict():
    """
        选择需要预测的域名,要求域名信息完整
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    s="select domain from domain_index where whois_flag=1 and locate_flag>0 and (other_info_flag=2 or other_info_flag=6)"
    print s
    cur.execute(s)
    while True:
        if domains.empty():
            r=cur.fetchmany(100)
            if len(r)==0:
                return
            for d in r:
                print "[add domain]: ",d
                domains.put(d[0])
        else:
            sleep(1)

def get_features():
    """
        从domains中取域名,加载其特征
    """
    while True:
        domain,judge_flag=domains.get(timeout=20)
        f=MalProbability.get_domain_features(domain)
        print domain,judge_flag,f
        samples.put([domain,judge_flag,f])

def write_to_csv(filename):
    """
        数据写入文件,不可多线程!
    """
    f=open(filename,'wb')
    w=csv.writer(f)
    w.writerow(['domain','judge_flag','keywords','http30x','alexa','locate','registrar','email_suffix'])
    while True:
        domain,judge_flag,f=samples.get(timeout=30)
        d=[domain,judge_flag]
        for item in f:
            d.append(item)
        w.writerow(d)

def load_data(filename=config.filename):
    # c=lambda:get_features()
    # p=lambda:get_domains()
    # model=ThreadEntry.ProduceConsumerModel(p,c,config={'produce_num':1,'consume_num':3})
    # model.prepare()
    # model.run()
    # model.join()
    write=lambda:write_to_csv(filename)

    first_model=ThreadEntry.ProduceConsumerModel(get_domains,get_features,config={'produce_num':1,'consume_num':3})
    second_model=ThreadEntry.ProduceConsumerModel(get_features,write,config={'produce_num':3,'consume_num':1})

    first_model.prepare()
    second_model.prepare()
    first_model.run()
    second_model.run()
    first_model.join()
    second_model.join()

def predict(filename):
    """
        调用决策树
    """
    tree,score=DecisionTree.build_decision_tree(filename)
    while True:
        domain=domains.get(timeout=30)
        predict=DecisionTree.predict(domain,tree)
        predicts.put([domain,predict])

def save_predict_todb():
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    s="UPDATE domain_index SET judge_flag=%s where ID=%s"
    sql=''
    while True:
        try:
            domain,flag=predicts.get(timeout=50)
            print domain,flag
            if flag[0]=='2':
                sql=s%(-1,hash(domain))
            elif flag[0]=='3':
                sql=s%(-1,hash(domain))
            elif flag[0]=='1':
                sql=s%(1,hash(domain))
            print sql
            # cur.execute(sql)
        except:
            # con.commit()
            raise

def do_predict():
    p=lambda:predict(sys.argv[1])

    first_model=ThreadEntry.ProduceConsumerModel(get_domain_to_predict,p,config={'produce_num':1,'consume_num':2})
    second_model=ThreadEntry.ProduceConsumerModel(p,save_predict_todb,config={'produce_num':2,'consume_num':2})

    first_model.prepare()
    second_model.prepare()
    first_model.run()
    second_model.run()
    first_model.join()
    second_model.join()

def main():
    #to initialize
    ConfigUpdater.update_config_on_locate()
    ConfigUpdater.update_config_on_alexa()

    #to load data
    # load_data(sys.argv[1])

    #to predict data
    do_predict()

if __name__=="__main__":

    main()
