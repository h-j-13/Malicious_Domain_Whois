#coding:utf-8

import redis
import threading
import exceptions
import requests
import config

#爬虫组给的代理获取接口
def _get_proxy():
    pool = redis.ConnectionPool(host='172.26.253.91', port=6379)
    r = redis.StrictRedis(connection_pool=pool, charset='utf-8')
    proxys_str = r.get("0")
    print proxys_str
    return eval(proxys_str)

class ProxyPool:
    """
        代理集合，提供耗时小的原子操作
    """
    def __init__(self):
        self.pool={}
        self.mutex=threading.Lock()

    def show(self):
        print "-------------"
        for key in self.pool:
            print key,self.pool[key]

    def add_proxy(self,proxy):
        self.mutex.acquire()
        self.pool[proxy]=0#标记为可用代理
        self.mutex.release()

    def delete_proxy(self,proxy):
        if proxy=="":
            return
        self.mutex.acquire()
        self.pool.pop(proxy)
        self.mutex.release()

    def get_proxy(self):
        self.mutex.acquire()
        for proxy in self.pool:
            if self.pool[proxy]==0:
                self.pool[proxy]=1#标记为代理正忙
                self.mutex.release()
                return proxy
        self.mutex.release()
        return ""

    def get_proxy_num(self):
        r=0
        for key in self.pool:
            if self.pool[key]==0:
                r+=1
        return r

    def free_proxy(self,proxy):
        if proxy=="":
            return
        self.mutex.acquire()
        if self.pool.has_key(proxy):
            self.pool[proxy]=0
        self.mutex.release()


class ProxyHelper:
    """
        负责和代理池的交互，负责耗时的代理操作(检测有效等),防止代理池长期被锁
    """
    def __init__(self):
        self.proxy_pool=ProxyPool()
        for item in config.my_proxys:
            self.proxy_pool.add_proxy(item)

    #测试代理是否有效
    def _test_proxyip(self,ip):
        try:
            proxy={'http':ip}
            res=requests.get("http://www.baidu.com",proxies=proxy,timeout=config.test_proxy_timeout)
            if res.content.find("百度一下")!=-1:
                return True
            else:
                return False
        except Exception,e:
            return False

    #添加一批代理并检测
    def add_more_proxyip(self):
        proxy_list=_get_proxy()
        #print proxy_list
        for item in proxy_list:
            if self._test_proxyip(item):
                print item,"avalible"
                self.proxy_pool.add_proxy(item)

    #输出当前代理池内代理数量
    def get_proxy_num(self):
        return self.proxy_pool.get_proxy_num()

    #获取一个代理
    def get_proxy(self):
        return self.proxy_pool.get_proxy()

    #删除一个代理
    def delete_proxy(self,proxy):
        self.proxy_pool.delete_proxy(proxy)

    #释放一个代理
    def free_proxy(self,proxy):
        self.proxy_pool.free_proxy(proxy)

    #展示代理情况
    def show_proxy(self):
        self.proxy_pool.show()

def main():
    proxy=ProxyHelper()
    # proxy.add_more_proxyip()
    proxy.show_proxy()
    p=proxy.get_proxy()
    proxy.show_proxy()
    proxy.delete_proxy(p)
    proxy.show_proxy()


if __name__=='__main__':
    main()
