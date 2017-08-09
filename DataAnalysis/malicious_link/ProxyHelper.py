#coding:utf-8
import requests
import redis
import threading
import exceptions

mutex=threading.Lock()

def _get_proxy():
    pool = redis.ConnectionPool(host='172.26.253.91', port=6379)
    r = redis.StrictRedis(connection_pool=pool, charset='utf-8')
    proxys_str = r.get("0")
    print proxys_str
    return eval(proxys_str)

class NoProxyAvaliable(exceptions.Exception):
    def __str__():
        print "代理ip不足"

class ProxyIP():
    #初始化，请求代理ip并筛选有效代理
    def __init__(self):
        self.proxy_ips={}

    #测试代理是否有效
    def _test_proxyip(self,ip):
        try:
            proxy={'http':ip}
	    #print "正在测试代理"
            res=requests.get("http://www.baidu.com",proxies=proxy,timeout=1)
            if res.content.find("百度一下")!=-1:
                return True
            else:
                return False
        except Exception,e:
	    #print e
            return False

    #添加代理ip并筛选
    def _add_more_proxyip(self):
        proxy_list=_get_proxy()
        for item in proxy_list:
            if self._test_proxyip(item):
                print "检测到可用代理"
		self.proxy_ips[item]=0#可用

    #返回代理
    def get_proxy(self):
        global mutex
        #mutex.acquire()
        for item in self.proxy_ips:
            if self.proxy_ips[item]==0:
                #print "----------"
                mutex.acquire()
                self.proxy_ips[item]=1
                mutex.release()
                #print "返回代理",item
                return item
        #print "返回代理","NONE"
        return ""
        #print "没有可用或空闲代理"
        #mutex.release()

    #释放代理，标记为可用
    def free_proxy(self,proxy):
        global mutex
        mutex.acquire()
        if proxy in self.proxy_ips:
            self.proxy_ips[proxy]=0
        mutex.release()

    #删除一个代理(无效)
    def delete_proxy(self,proxy):
        global mutex
        mutex.acquire()
        if self.proxy_ips.has_key(proxy):
            del self.proxy_ips[proxy]
        mutex.release()

    def get_proxy_num(self):
        global mutex,IS_DEBUG
        mutex.acquire()
        num=len(self.proxy_ips)
        mutex.release()
        return num

    #返回可用代理数量
    def get_free_proxy_num(self):
        global mutex,IS_DEBUG
        mutex.acquire()
        if len(self.proxy_ips)==0:
            mutex.release()
            return 0
        num=0
        for item in self.proxy_ips:
            if self.proxy_ips[item]==0:
                num+=1
		print "检测到可用代理"
        mutex.release()
        return num
