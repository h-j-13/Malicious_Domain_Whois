#!coding:utf-8

"""
    这是一个生产者-消费者模型,适用于以下场景:
        1. 将大量数据快速提交给数据库
        2. 大规模探测任务
"""

import threading

class ProduceConsumerModel:
    """
        模型,内部不保存任何状态,可重复计算
    """
    def __init__(self,produce_func,consume_func,config={'produce_num':3,'consume_num':1}):
        self.__produce_functor=produce_func
        self.__consume_functor=consume_func
        self.__produce_threads=[]
        self.__consume_threads=[]
        self.__produce_num=config['produce_num']
        self.__consume_num=config['consume_num']

    def prepare(self):
        """
            按配置准备好各线程
        """
        for _ in range(self.__produce_num):
            self.__produce_threads.append(threading.Thread(target=self.__produce_functor))
        for _ in range(self.__consume_num):
            self.__consume_threads.append(threading.Thread(target=self.__consume_functor))

    def run(self):
        """
            启动所有线程,开始工作,所有线程完成工作后推出
        """
        try:
            for td in self.__produce_threads:
                td.start()
            for td in self.__consume_threads:
                td.start()
        except Exception,e:
            raise

    def join(self):
        try:
            for td in self.__consume_threads:
                td.join()
            for td in self.__produce_threads:
                td.join()
        except Exception,e:
            raise
