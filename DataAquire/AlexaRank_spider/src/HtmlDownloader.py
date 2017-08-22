#coding:utf-8

"""
    负责下载网页，同时处理反爬虫
"""

import requests
import config
import exceptions

class HtmlDownloadError(Exception):
    def __str__():
        print "自定义异常：下载网页失败"

def download_alex_rank_html(domain,proxy=""):
    """
        这一环节的错误只可能出自代理和下载过程，无法得到域名是否可访问
        如果发生错误，返回空网页
    """
    try:
        print "正在下载",domain,proxy
        proxy={'http':proxy}
        url="http://alexa.chinaz.com/"+domain
        #print url,"proxy:",proxy
        res=requests.get(url,proxies=proxy,timeout=config.download_alex_rank_timeout)
        #print res.content
        if res.content.find("Alexa网站排名查询")==-1:
            return ""
        if config.save_response:
            file=open(config.path_to_save+"alex-rank/"+domain+".html",'w')
            file.write(str(res.headers))
            file.write(str(res.content))
            file.close()
        return res.content
    except Exception,e:
        print e
        raise

def download_alex_judge_html(domain,proxy=""):
    proxy={'http':proxy}
    try:
        print "正在下载",domain,proxy
        url="http://tool.chinaz.com/webscan/?host="+domain
        res=requests.get(url,proxies=proxy,timeout=config.download_alex_judge_timeout)
        if res.content.find("网站安全检测结果")==-1:
            return ""
        if config.save_response:
            file=open(config.path_to_save+"alex-judge/"+domain+".html",'w')
            file.write(str(res.headers))
            file.write(str(res.content))
            file.close()
        return res.content
    except Exception,e:
        raise

html_downloader={"alex-judge":download_alex_judge_html,"alex-rank":download_alex_rank_html}

def main():
    #print download_alex_rank_html("www.taobao.com")
    print download_alex_judge_html("www.taobao.com")

if __name__=="__main__":
    main()
